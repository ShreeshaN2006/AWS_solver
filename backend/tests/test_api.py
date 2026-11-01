from fastapi.testclient import TestClient

from app.api import routes
from app.main import app


client = TestClient(app)


def test_dashboard_endpoint():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_modules"] == 10
    assert payload["course_title"] == "AWS Academy Cloud Foundations"


def test_progress_and_study_plan_flow():
    update = {
        "item_id": "m1-item-1",
        "module_id": "m1",
        "status": "In Progress",
    }
    response = client.post("/api/progress/record", json=update)
    assert response.status_code == 200
    plan = client.post("/api/study-plan", json={"available_time": "60 minutes"})
    assert plan.status_code == 200
    assert plan.json()["schedule"]


def test_tutor_passes_full_retrieved_context_to_provider(monkeypatch):
    source = {
        "module": "AWS Cloud Security",
        "document": "security-notes.pdf",
        "page_number": 3,
        "timestamp": None,
        "source_url": None,
    }
    course_excerpt = "AWS IAM policies define allowed actions for principals."

    monkeypatch.setattr(
        routes.agent_tools,
        "explain_topic",
        lambda question, module_id=None: {
            "context": f"[Source 1: AWS Cloud Security | security-notes.pdf | page 3]\n{course_excerpt}",
            "sources": [source],
        },
    )

    class FakeProvider:
        def respond(self, prompt, context):
            assert prompt == "What do IAM policies do?"
            assert course_excerpt in context
            return "They define which actions a principal is allowed to perform."

    monkeypatch.setattr(routes, "get_llm_provider", lambda: FakeProvider())
    response = client.post(
        "/api/tutor/ask",
        json={"question": "What do IAM policies do?", "module_id": "m4"},
    )

    assert response.status_code == 200
    assert response.json()["answer"].startswith("They define")
    assert response.json()["sources"][0]["page_number"] == 3
