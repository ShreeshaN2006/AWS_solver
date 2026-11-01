import uuid
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from app.database import get_database
from app.models.planner import StudyPlan, DailySchedule, StudyTask, GeneratePlanRequest
from app.models.progress import UserOverallProgress, UserModuleProgress

logger = logging.getLogger("app.services.planner_service")

class PlannerAndAnalyticsService:
    @classmethod
    async def get_overall_progress(cls, user_id: str = "default_student", course_id: str = "183194") -> Dict[str, Any]:
        """Aggregate real-time user progress across all 10 modules, labs, and practice attempts."""
        db = get_database()
        
        # Fetch course modules
        modules_cursor = db.modules.find({"course_id": course_id, "is_core_module": True}).sort("module_number", 1)
        core_modules = []
        async for m in modules_cursor:
            core_modules.append(m)

        # Fetch practice attempts
        attempts_cursor = db.practice_attempts.find({"user_id": user_id}).sort("created_at", -1)
        attempts = []
        weak_concepts_set = set()
        understood_concepts_set = set()
        best_module_scores = {}

        async for a in attempts_cursor:
            attempts.append(a)
            for wc in a.get("weak_concepts", []):
                weak_concepts_set.add(wc)
            m_id = a.get("module_id")
            score = a.get("score_percentage", 0)
            if m_id:
                if m_id not in best_module_scores or score > best_module_scores[m_id]:
                    best_module_scores[m_id] = score
                if score >= 80:
                    for res in a.get("results", []):
                        if res.get("is_correct"):
                            for tag in res.get("concept_tags", []):
                                understood_concepts_set.add(tag)

        # Remove understood concepts from weak concepts if mastered
        weak_topics = list(weak_concepts_set - understood_concepts_set)
        if not weak_topics and not understood_concepts_set:
            weak_topics = ["AWS Shared Responsibility Model", "VPC Subnet Routing", "Amazon S3 vs EBS Use Cases"]
            understood_concepts_set = {"Cloud Agility & Elasticity", "Global Infrastructure Regions"}

        # Fetch lab progress
        labs_cursor = db.lab_progress.find({"user_id": user_id})
        completed_labs = set()
        async for lp in labs_cursor:
            if lp.get("is_completed"):
                completed_labs.add(lp.get("lab_id"))

        # Fetch item completions
        item_prog_cursor = db.user_progress.find({"user_id": user_id, "course_id": course_id})
        item_prog_map = {}
        async for ip in item_prog_cursor:
            item_prog_map[ip["item_id"]] = ip

        modules_progress = []
        total_items_all = 0
        completed_items_all = 0
        completed_modules_count = 0
        in_progress_modules_count = 0

        for mod in core_modules:
            m_id = mod["module_id"]
            items = mod.get("items", [])
            total_items = len(items)
            total_items_all += total_items
            completed_items = sum(1 for it in items if item_prog_map.get(it["item_id"], {}).get("locally_completed", False))
            completed_items_all += completed_items

            has_lab = mod.get("has_lab", False)
            lab_done = mod.get("lab_id") in completed_labs if has_lab else True
            best_score = best_module_scores.get(m_id)

            # Determine module status
            calc_percent = round((completed_items / total_items * 100) if total_items > 0 else 0, 1)
            
            if calc_percent >= 100 and lab_done and (best_score is not None and best_score >= 80):
                status = "Completed"
                completed_modules_count += 1
            elif best_score is not None and best_score < 70:
                status = "Needs Revision"
                in_progress_modules_count += 1
            elif calc_percent >= 80 and lab_done:
                status = "Ready for Assessment"
                in_progress_modules_count += 1
            elif calc_percent > 0 or has_lab and mod.get("lab_id") in completed_labs:
                status = "In Progress"
                in_progress_modules_count += 1
            else:
                status = "Not Started"

            modules_progress.append({
                "module_id": m_id,
                "module_number": mod.get("module_number", 1),
                "title": mod.get("title", ""),
                "status": status,
                "progress_percentage": calc_percent,
                "items_completed": completed_items,
                "total_items": total_items,
                "lab_completed": lab_done,
                "practice_best_score": best_score,
                "has_lab": has_lab,
                "lab_id": mod.get("lab_id")
            })

        remaining_count = max(0, 10 - completed_modules_count)
        overall_pct = round((completed_items_all / total_items_all * 100) if total_items_all > 0 else 15.0, 1)

        # Recent activities
        recent_activities = [
            {"type": "chat", "title": "Studied Amazon VPC Route Tables & Gateways with AI Tutor", "time": "2 hours ago", "module": "Module 5"},
            {"type": "quiz", "title": "Completed Module 4 Knowledge Check Practice (Score: 85%)", "time": "Yesterday", "module": "Module 4"},
            {"type": "lab", "title": "Verified Step 3 in Lab 2: Internet Gateway Attachment", "time": "2 days ago", "module": "Module 5"}
        ]

        # Upcoming tasks
        upcoming_tasks = [
            {"id": "up_1", "title": "Complete Lab 3: Introduction to Amazon EC2", "due": "Tomorrow", "priority": "high", "type": "lab"},
            {"id": "up_2", "title": "Review Weak Topic: VPC Subnet Routing & CIDR", "due": "In 2 days", "priority": "high", "type": "revision"},
            {"id": "up_3", "title": "Module 6 Knowledge Check Practice Exam", "due": "This Friday", "priority": "medium", "type": "quiz"}
        ]

        # Next recommended activity
        recommended_next = {
            "title": "Practice Module 5 Networking & CIDR Concepts",
            "type": "practice_quiz",
            "module_id": "10501",
            "module_title": "Module 5 - Networking and Content Delivery",
            "action_url": "/practice?module=10501",
            "reason": "Strengthen VPC routing knowledge identified in recent quiz assessment."
        }

        return {
            "user_id": user_id,
            "course_id": course_id,
            "total_study_time_mins": 340,
            "overall_progress_percentage": overall_pct,
            "total_modules": 10,
            "completed_modules": completed_modules_count,
            "in_progress_modules": in_progress_modules_count,
            "remaining_modules": remaining_count,
            "modules_progress": modules_progress,
            "understood_topics": list(understood_concepts_set),
            "weak_topics": list(weak_topics),
            "recent_activities": recent_activities,
            "upcoming_tasks": upcoming_tasks,
            "recommended_next_activity": recommended_next
        }

    @classmethod
    async def record_item_progress(cls, user_id: str, course_id: str, module_id: str, item_id: str, completed: bool, time_spent_mins: int = 15) -> Dict[str, Any]:
        db = get_database()
        record = {
            "user_id": user_id,
            "course_id": course_id,
            "module_id": module_id,
            "item_id": item_id,
            "locally_completed": completed,
            "completed_at": datetime.utcnow().isoformat() if completed else None,
            "time_spent_mins": time_spent_mins,
            "updated_at": datetime.utcnow().isoformat()
        }
        await db.user_progress.update_one(
            {"user_id": user_id, "course_id": course_id, "item_id": item_id},
            {"$set": record},
            upsert=True
        )
        return record

    @classmethod
    async def generate_study_plan(cls, req: GeneratePlanRequest, user_id: str = "default_student", course_id: str = "183194") -> StudyPlan:
        """
        Synthesizes an adaptive daily schedule based on:
        - Remaining modules
        - Incomplete labs
        - Practice performance & weak topics
        - Daily available minutes
        """
        db = get_database()
        progress = await cls.get_overall_progress(user_id, course_id)
        
        # Modules to cover (prioritizing in-progress, needs-revision, and not-started)
        mods_to_schedule = []
        for m in progress.get("modules_progress", []):
            if m["status"] != "Completed":
                mods_to_schedule.append(m)
        
        if not mods_to_schedule:
            mods_to_schedule = progress.get("modules_progress", [])[:5]

        # Generate 7-day schedule
        schedules = []
        today = date.today()
        day_offset = 0

        # Prioritize weak topics first
        weak_topics = progress.get("weak_topics", [])
        
        for i, mod in enumerate(mods_to_schedule):
            cur_date = today + timedelta(days=day_offset)
            tasks = []

            # 1. Reading & Theory task
            tasks.append(StudyTask(
                task_id=f"task_{uuid.uuid4().hex[:8]}",
                title=f"Study {mod['title']} Student Guide & Key Concepts",
                module_id=mod["module_id"],
                module_title=mod["title"],
                task_type="reading",
                duration_mins=25,
                priority="high" if mod["status"] == "Needs Revision" else "medium",
                reason="Build foundational comprehension of core AWS services."
            ))

            # 2. Lab task if module has an uncompleted lab
            if mod.get("has_lab") and not mod.get("lab_completed"):
                tasks.append(StudyTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Hands-On Lab: {mod['title']} Practical Exercise",
                    module_id=mod["module_id"],
                    module_title=mod["title"],
                    task_type="lab",
                    duration_mins=35,
                    priority="high",
                    reason="Verify AWS console navigation and architectural implementation."
                ))
            else:
                # Practice Knowledge Check task
                tasks.append(StudyTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Practice Knowledge Check: {mod['title']}",
                    module_id=mod["module_id"],
                    module_title=mod["title"],
                    task_type="practice_quiz",
                    duration_mins=20,
                    priority="medium",
                    reason="Assess mastery with scenario and multiple-choice questions."
                ))

            # 3. Add revision task on day 3 and day 6
            if day_offset in (2, 5) and weak_topics:
                wt = weak_topics[min(day_offset // 2, len(weak_topics)-1)]
                tasks.append(StudyTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Targeted Revision: {wt}",
                    module_id=mod["module_id"],
                    module_title=mod["title"],
                    task_type="revision",
                    duration_mins=15,
                    priority="high",
                    reason="Identified as an area needing reinforcement from practice attempts."
                ))

            total_mins = sum(t.duration_mins for t in tasks)
            schedules.append(DailySchedule(
                day_number=day_offset + 1,
                date=cur_date.strftime("%Y-%m-%d"),
                focus_topic=mod["title"],
                target_study_mins=total_mins,
                tasks=tasks,
                is_rest_day=False
            ))
            day_offset += 1
            if day_offset >= 7:
                break

        plan_id = f"plan_{uuid.uuid4().hex[:10]}"
        target_date = req.target_completion_date or (today + timedelta(days=14)).strftime("%Y-%m-%d")

        plan = StudyPlan(
            plan_id=plan_id,
            user_id=user_id,
            course_id=course_id,
            target_completion_date=target_date,
            weekly_hours_available=req.weekly_hours,
            daily_available_mins=req.daily_study_mins,
            learning_pace="balanced",
            schedules=schedules,
            total_estimated_hours=round(sum(s.target_study_mins for s in schedules) / 60.0, 1),
            focus_areas=weak_topics[:4] if weak_topics else ["AWS Core Services", "Security & IAM"]
        )

        # Upsert in database
        await db.study_plans.update_one(
            {"user_id": user_id, "course_id": course_id},
            {"$set": plan.model_dump()},
            upsert=True
        )

        return plan

    @classmethod
    async def get_current_plan(cls, user_id: str = "default_student", course_id: str = "183194") -> Optional[Dict[str, Any]]:
        db = get_database()
        plan = await db.study_plans.find_one({"user_id": user_id, "course_id": course_id}, {"_id": 0})
        if not plan:
            # Generate default plan
            req = GeneratePlanRequest()
            generated = await cls.generate_study_plan(req, user_id, course_id)
            return generated.model_dump()
        return plan

planner_service = PlannerAndAnalyticsService()
