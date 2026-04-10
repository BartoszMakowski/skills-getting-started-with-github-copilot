def test_get_activities_returns_200_and_dict(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_activities_contains_expected_fields(client):
    response = client.get("/activities")
    payload = response.json()

    assert payload, "Activities payload should not be empty"
    for activity in payload.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity


def test_get_activities_participants_is_list(client):
    payload = client.get("/activities").json()

    for activity in payload.values():
        assert isinstance(activity["participants"], list)


def test_get_activities_reflects_signup_mutation(client):
    email = "test.student@mergington.edu"
    activity_name = "Chess Club"

    signup = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup.status_code == 200

    payload = client.get("/activities").json()
    assert email in payload[activity_name]["participants"]
