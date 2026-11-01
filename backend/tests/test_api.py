import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import DatabaseManager
from app.seed_data.course_seed import seed_course_data
from app.seed_data.practice_seed import seed_practice_questions
from app.services.lab_service import lab_service

@pytest.mark.asyncio
async def test_full_api_endpoints():
    await DatabaseManager.connect()
    await seed_course_data()
    await seed_practice_questions()
    await lab_service.init_seed_labs()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        
        # 1. Health check
        res = await client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["service"] == "AWS Academy Course Copilot"
        assert data["mongodb_connected"] is True

        # 2. Course details & modules
        res = await client.get("/api/courses/183194")
        assert res.status_code == 200
        course = res.json()
        assert course["course_id"] == "183194"
        assert len(course["modules"]) >= 10

        res_mods = await client.get("/api/courses/183194/modules?core_only=true")
        assert res_mods.status_code == 200
        core_mods = res_mods.json()
        assert len(core_mods) == 10

        # 3. AI Tutor Chat with citations
        res_chat = await client.post("/api/chat/message", json={
            "message": "Explain Amazon S3 vs EBS and provide citations.",
            "module_id": "10701"
        })
        assert res_chat.status_code == 200
        chat_body = res_chat.json()
        assert "message" in chat_body
        assert len(chat_body["citations"]) > 0

        # 4. Knowledge Check Practice
        res_q = await client.get("/api/practice/questions?module_id=10101")
        assert res_q.status_code == 200
        questions = res_q.json()
        assert len(questions) > 0

        # Submit practice answer
        q0 = questions[0]
        res_sub = await client.post("/api/practice/submit", json={
            "module_id": "10101",
            "is_comprehensive_exam": False,
            "answers": [
                {"question_id": q0["question_id"], "selected_option_id": q0["correct_option_id"]}
            ],
            "time_spent_seconds": 60
        })
        assert res_sub.status_code == 200
        attempt = res_sub.json()
        assert attempt["score_percentage"] == 100.0
        assert attempt["correct_count"] == 1

        # 5. AWS Labs
        res_labs = await client.get("/api/labs")
        assert res_labs.status_code == 200
        labs = res_labs.json()
        assert len(labs) == 6

        # Lab step confirmation
        res_conf = await client.post("/api/labs/lab_1/steps/1/confirm", json={"confirmed": True})
        assert res_conf.status_code == 200
        assert 1 in res_conf.json()["completed_steps"]

        # Lab troubleshooting
        res_tb = await client.post("/api/labs/troubleshoot", json={
            "lab_id": "lab_1",
            "step_number": 2,
            "error_message": "AccessDenied: User is not authorized to perform: iam:CreateGroup",
            "user_description": "Cannot create S3-Support group"
        })
        assert res_tb.status_code == 200
        tb = res_tb.json()
        assert "IAM Authorization Denied" in tb["diagnosis"]

        # 6. Progress Analytics
        res_prog = await client.get("/api/progress/analytics")
        assert res_prog.status_code == 200
        prog = res_prog.json()
        assert prog["total_modules"] == 10
        assert len(prog["modules_progress"]) == 10

        # 7. Study Planner
        res_plan = await client.get("/api/planner/current")
        assert res_plan.status_code == 200
        plan = res_plan.json()
        assert len(plan["schedules"]) > 0

        # 8. Canvas Status
        res_canvas = await client.get("/api/canvas/status")
        assert res_canvas.status_code == 200
        assert res_canvas.json()["course_id"] == "183194"

        # 9. Settings
        res_sett = await client.get("/api/settings")
        assert res_sett.status_code == 200
        assert res_sett.json()["llm_provider"] is not None

        # 10. Canvas HTML Import
        with open("sample_data/aws_academy_canvas_export.html", "rb") as f:
            res_imp = await client.post(
                "/api/documents/import-canvas-html",
                files={"file": ("aws_academy_canvas_export.html", f, "text/html")}
            )
        assert res_imp.status_code == 200
        assert res_imp.json()["details"]["modules_imported"] >= 10

    await DatabaseManager.close()
