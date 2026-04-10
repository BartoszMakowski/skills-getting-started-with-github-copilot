def test_signup_success_adds_participant(client):
    email = "new.student@mergington.edu"
    activity_name = "Basketball Team"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "a@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_signup(client):
    email = "alex@mergington.edu"
    activity_name = "Basketball Team"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_response_message_format(client):
    email = "format.check@mergington.edu"
    activity_name = "Debate Team"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_allows_empty_email_with_current_api_behavior(client):
    activity_name = "Art Studio"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": ""})

    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert "" in activities[activity_name]["participants"]


def test_signup_allows_non_email_string_with_current_api_behavior(client):
    raw_value = "not-an-email"
    activity_name = "Soccer Club"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": raw_value})

    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert raw_value in activities[activity_name]["participants"]
