"""Autonomous course execution engine.

This service turns discovered Canvas/course state into durable tasks and runs a
controlled execution loop. It deliberately separates planning from execution:
read-only discovery, knowledge work, progress bookkeeping, and verification may
run automatically; authentication, destructive/costly AWS actions, and final
graded submissions are surfaced as human interventions.
"""
from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import get_database
from app.services.canvas_api import canvas_service
from app.config import settings

logger = logging.getLogger("app.services.autonomous_agent")


RUN_STATES = {"idle", "running", "paused", "stopped", "waiting_for_user", "completed", "failed"}
TASK_STATES = {"queued", "running", "waiting_for_user", "completed", "failed", "skipped"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AutonomousCourseAgent:
    """Durable planner/executor for one user/course pair."""

    def __init__(self, user_id: str = "default_student", course_id: str = "183194"):
        self.user_id = user_id
        self.course_id = course_id
        self._stop_events: Dict[str, asyncio.Event] = {}
        self._pause_events: Dict[str, asyncio.Event] = {}
        self._workers: Dict[str, asyncio.Task] = {}

    async def _db(self):
        return get_database()

    async def get_run(self) -> Optional[Dict[str, Any]]:
        db = await self._db()
        return await db.agent_runs.find_one(
            {"user_id": self.user_id, "course_id": self.course_id}, {"_id": 0}
        )

    async def discover_and_plan(self, run_id: str) -> Dict[str, Any]:
        """Discover live Canvas state and create idempotent durable tasks."""
        db = await self._db()
        modules = await canvas_service.fetch_course_modules(self.course_id)
        assignments = await canvas_service.fetch_assignments(self.course_id)

        # Replace the discovered snapshot, preserving historical run/task data.
        await db.agent_discovery.update_one(
            {"user_id": self.user_id, "course_id": self.course_id},
            {"$set": {
                "user_id": self.user_id,
                "course_id": self.course_id,
                "modules": modules,
                "assignments": assignments,
                "discovered_at": now(),
                "run_id": run_id,
            }},
            upsert=True,
        )

        created = 0
        tasks: List[Dict[str, Any]] = []
        for module_index, module in enumerate(modules):
            module_id = str(module.get("id", module.get("module_id", f"module-{module_index}")))
            items = module.get("items") or []
            for item_index, item in enumerate(items):
                item_id = str(item.get("id", item.get("item_id", f"item-{item_index}")))
                completion = (item.get("content_details") or {}).get("completion_requirement")
                # Canvas completion is evidence, not a locally guessed completion.
                completed = bool(
                    item.get("completed") is True
                    or item.get("completion_state") in {"completed", "complete"}
                )
                task_key = f"canvas:{self.course_id}:module:{module_id}:item:{item_id}"
                task = {
                    "task_id": str(uuid.uuid5(uuid.NAMESPACE_URL, task_key)),
                    "task_key": task_key,
                    "run_id": run_id,
                    "user_id": self.user_id,
                    "course_id": self.course_id,
                    "module_id": module_id,
                    "title": item.get("title") or item.get("name") or f"Canvas item {item_id}",
                    "item_type": item.get("type") or item.get("content_type") or "unknown",
                    "canvas_item_id": item_id,
                    "completion_requirement": completion,
                    "state": "completed" if completed else "queued",
                    "automation": self._automation_class(item),
                    "priority": module_index * 100 + item_index,
                    "created_at": now(),
                    "updated_at": now(),
                }
                await db.agent_tasks.update_one(
                    {"task_key": task_key, "user_id": self.user_id},
                    {"$setOnInsert": task},
                    upsert=True,
                )
                tasks.append(task)
                created += 1

        # Assignments not represented as module items are still visible to the planner.
        for assignment in assignments:
            assignment_id = str(assignment.get("id"))
            if assignment_id == "None":
                continue
            task_key = f"canvas:{self.course_id}:assignment:{assignment_id}"
            task = {
                "task_id": str(uuid.uuid5(uuid.NAMESPACE_URL, task_key)),
                "task_key": task_key,
                "run_id": run_id,
                "user_id": self.user_id,
                "course_id": self.course_id,
                "title": assignment.get("name", f"Assignment {assignment_id}"),
                "item_type": "assignment",
                "canvas_item_id": assignment_id,
                "state": "queued",
                "automation": "human_review",
                "priority": 10000,
                "created_at": now(),
                "updated_at": now(),
            }
            await db.agent_tasks.update_one(
                {"task_key": task_key, "user_id": self.user_id},
                {"$setOnInsert": task},
                upsert=True,
            )

        await db.agent_runs.update_one(
            {"run_id": run_id},
            {"$set": {"phase": "planned", "last_discovery_at": now(), "planned_task_count": created}},
        )
        return {"modules": len(modules), "assignments": len(assignments), "tasks_discovered": created}

    @staticmethod
    def _automation_class(item: Dict[str, Any]) -> str:
        kind = str(item.get("type") or item.get("content_type") or "").lower()
        if kind in {"page", "file", "externalurl", "external_tool", "contextmodule"}:
            return "coursework"
        if "quiz" in kind:
            return "human_review"
        if "assignment" in kind:
            return "human_review"
        return "coursework"

    async def start(self, dry_run: bool = True) -> Dict[str, Any]:
        current = await self.get_run()
        if current and current.get("state") == "running":
            return current

        run_id = f"run_{uuid.uuid4().hex[:12]}"
        db = await self._db()
        run = {
            "run_id": run_id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "state": "running",
            "phase": "discovering",
            "dry_run": dry_run,
            "started_at": now(),
            "updated_at": now(),
            "current_task_id": None,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "waiting_tasks": 0,
            "last_error": None,
        }
        await db.agent_runs.update_one(
            {"user_id": self.user_id, "course_id": self.course_id},
            {"$set": run},
            upsert=True,
        )
        self._stop_events[run_id] = asyncio.Event()
        self._pause_events[run_id] = asyncio.Event()
        self._pause_events[run_id].set()
        self._workers[run_id] = asyncio.create_task(self._run_loop(run_id))
        return run

    async def pause(self) -> Dict[str, Any]:
        run = await self.get_run()
        if not run or run.get("state") not in {"running", "waiting_for_user"}:
            return run or {"state": "idle"}
        event = self._pause_events.get(run["run_id"])
        if event:
            event.clear()
        db = await self._db()
        await db.agent_runs.update_one({"run_id": run["run_id"]}, {"$set": {"state": "paused", "updated_at": now()}})
        return await self.get_run()

    async def resume(self) -> Dict[str, Any]:
        run = await self.get_run()
        if not run:
            return {"state": "idle"}
        event = self._pause_events.setdefault(run["run_id"], asyncio.Event())
        event.set()
        db = await self._db()
        await db.agent_runs.update_one({"run_id": run["run_id"]}, {"$set": {"state": "running", "updated_at": now()}})
        if run["run_id"] not in self._workers or self._workers[run["run_id"]].done():
            self._stop_events.setdefault(run["run_id"], asyncio.Event()).clear()
            self._workers[run["run_id"]] = asyncio.create_task(self._run_loop(run["run_id"]))
        return await self.get_run()

    async def stop(self) -> Dict[str, Any]:
        run = await self.get_run()
        if not run:
            return {"state": "idle"}
        stop_event = self._stop_events.setdefault(run["run_id"], asyncio.Event())
        stop_event.set()
        pause = self._pause_events.get(run["run_id"])
        if pause:
            pause.set()
        db = await self._db()
        await db.agent_runs.update_one({"run_id": run["run_id"]}, {"$set": {"state": "stopped", "updated_at": now()}})
        return await self.get_run()

    async def _run_loop(self, run_id: str) -> None:
        db = await self._db()
        stop_event = self._stop_events[run_id]
        pause_event = self._pause_events[run_id]
        try:
            await self.discover_and_plan(run_id)
            while not stop_event.is_set():
                await pause_event.wait()
                run = await db.agent_runs.find_one({"run_id": run_id}, {"_id": 0})
                if not run or run.get("state") == "stopped":
                    return

                task = await db.agent_tasks.find_one(
                    {"run_id": run_id, "user_id": self.user_id, "state": "queued"},
                    {"_id": 0},
                    sort=[("priority", 1), ("created_at", 1)],
                )
                if not task:
                    await db.agent_runs.update_one({"run_id": run_id}, {"$set": {"state": "completed", "phase": "complete", "updated_at": now()}})
                    return

                await db.agent_tasks.update_one({"task_id": task["task_id"]}, {"$set": {"state": "running", "started_at": now(), "updated_at": now()}})
                await db.agent_runs.update_one({"run_id": run_id}, {"$set": {"current_task_id": task["task_id"], "phase": "executing", "updated_at": now()}})
                result = await self._execute_task(task, bool(run.get("dry_run", True)))
                await db.agent_tasks.update_one(
                    {"task_id": task["task_id"]},
                    {"$set": {"state": result["state"], "result": result, "updated_at": now()}},
                )
                if result["state"] == "waiting_for_user":
                    await db.agent_runs.update_one(
                        {"run_id": run_id},
                        {"$set": {"state": "waiting_for_user", "waiting_tasks": 1, "updated_at": now()}},
                    )
                    return
                if result["state"] == "failed":
                    await db.agent_runs.update_one(
                        {"run_id": run_id},
                        {"$inc": {"failed_tasks": 1}, "$set": {"last_error": result.get("error"), "updated_at": now()}},
                    )
                else:
                    await db.agent_runs.update_one(
                        {"run_id": run_id},
                        {"$inc": {"completed_tasks": 1}, "$set": {"updated_at": now()}},
                    )
                await asyncio.sleep(0)
        except Exception as exc:
            logger.exception("Autonomous run %s failed", run_id)
            await db.agent_runs.update_one(
                {"run_id": run_id},
                {"$set": {"state": "failed", "phase": "error", "last_error": str(exc), "updated_at": now()}},
            )

    async def _execute_task(self, task: Dict[str, Any], dry_run: bool) -> Dict[str, Any]:
        automation = task.get("automation")
        if automation == "human_review":
            return {
                "state": "waiting_for_user",
                "reason": "This activity may be graded or require an explicit student decision before submission.",
                "requires_user": True,
            }
        if dry_run:
            return {"state": "completed", "mode": "dry_run", "action": "planned", "verified": False}
        # Phase 1 intentionally executes only safe internal bookkeeping. Canvas write
        # operations and AWS resource mutations are separate tools gated by approval.
        return {
            "state": "completed",
            "mode": "safe_execution",
            "action": "coursework_task_registered",
            "verified": False,
            "note": "Execution framework is active; external mutation tools require explicit approval gates.",
        }


_agents: Dict[tuple[str, str], AutonomousCourseAgent] = {}


def get_autonomous_agent(user_id: str = "default_student", course_id: str = "183194") -> AutonomousCourseAgent:
    key = (user_id, course_id)
    if key not in _agents:
        _agents[key] = AutonomousCourseAgent(user_id, course_id)
    return _agents[key]
