import pytest

from app.services.autonomous_agent import AutonomousCourseAgent


def test_automation_classification():
    assert AutonomousCourseAgent._automation_class({"type": "Page"}) == "coursework"
    assert AutonomousCourseAgent._automation_class({"type": "File"}) == "coursework"
    assert AutonomousCourseAgent._automation_class({"type": "Quiz"}) == "human_review"
    assert AutonomousCourseAgent._automation_class({"type": "Assignment"}) == "human_review"


@pytest.mark.asyncio
async def test_execute_task_dry_run():
    agent = AutonomousCourseAgent()
    result = await agent._execute_task({"automation": "coursework"}, dry_run=True)
    assert result["state"] == "completed"
    assert result["mode"] == "dry_run"


@pytest.mark.asyncio
async def test_execute_task_requires_human_review():
    agent = AutonomousCourseAgent()
    result = await agent._execute_task({"automation": "human_review"}, dry_run=False)
    assert result["state"] == "waiting_for_user"
    assert result["requires_user"] is True
