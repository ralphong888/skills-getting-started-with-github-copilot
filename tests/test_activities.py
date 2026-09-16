import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]


def test_unregister_participant_removes_email_from_activity():
    reset_activities()
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "daniel@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404():
    reset_activities()
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "not-a-student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
