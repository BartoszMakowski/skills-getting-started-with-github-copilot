def test_delete_signup_success_removes_participant(client):
    email = "alex@mergington.edu"
    activity_name = "Basketball Team"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_delete_signup_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/signup", params={"email": "a@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_signup_returns_400_when_not_registered(client):
    response = client.delete("/activities/Chess%20Club/signup", params={"email": "notthere@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_delete_signup_removes_recently_added_participant(client):
    email = "temp.delete@mergington.edu"
    activity_name = "Programming Class"

    signup = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup.status_code == 200

    remove = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    assert remove.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_delete_signup_second_attempt_returns_400(client):
    email = "alex@mergington.edu"
    activity_name = "Basketball Team"

    first = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    second = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Student is not signed up for this activity"
