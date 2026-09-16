import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Soccer Club"]["participants"] = []


def test_signup_for_activity_adds_participant():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.post(
        "/activities/Soccer Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Soccer Club"
    assert "newstudent@mergington.edu" in activities["Soccer Club"]["participants"]


def test_signup_for_activity_rejects_duplicate_email():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "daniel@mergington.edu"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "not-a-student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
