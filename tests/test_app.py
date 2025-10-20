from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # ensure keys exist and are a dict
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure not already registered
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup should succeed
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    res_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert res_dup.status_code == 400

    # Cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)


def test_remove_participant():
    activity = "Programming Class"
    email = "remove_me@example.com"

    # Ensure participant is present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Remove via API
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert email not in activities[activity]["participants"]

    # Removing again should produce 400
    res_again = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res_again.status_code == 400
