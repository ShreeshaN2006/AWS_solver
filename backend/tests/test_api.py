from fastapi.testclient import TestClient

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
