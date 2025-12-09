from fastapi.testclient import TestClient
from src import app as app_module

client = TestClient(app_module.app)


def test_signup_and_unregister_flow():
    activity_name = "Chess Club"
    test_email = "pytest-user@example.com"

    # Ensure activity exists
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    assert activity_name in activities

    participants_before = list(activities[activity_name]["participants"])

    # Sign up the test user
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup_resp.status_code == 200
    assert test_email in signup_resp.json().get("message", "")

    # Verify participant was added
    resp_after = client.get("/activities")
    assert resp_after.status_code == 200
    activities_after = resp_after.json()
    assert test_email in activities_after[activity_name]["participants"]

    # Unregister the test user
    del_resp = client.delete(f"/activities/{activity_name}/participants?email={test_email}")
    assert del_resp.status_code == 200
    assert test_email in del_resp.json().get("message", "")

    # Verify participant was removed
    resp_final = client.get("/activities")
    assert resp_final.status_code == 200
    activities_final = resp_final.json()
    assert test_email not in activities_final[activity_name]["participants"]

    # Cleanup: ensure we didn't remove any original participants
    # (participants_before should be a subset of final participants)
    for p in participants_before:
        assert p in activities_final[activity_name]["participants"]
