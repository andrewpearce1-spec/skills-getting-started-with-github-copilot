from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    # Arrange: No special setup needed

    # Act: Make GET request to root endpoint without following redirects
    response = client.get("/", follow_redirects=False)

    # Assert: Should redirect to static index.html
    assert response.status_code == 302
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    # Arrange: No special setup needed

    # Act: Make GET request to activities endpoint
    response = client.get("/activities")

    # Assert: Should return 200 and activities dict
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]


def test_signup_success():
    # Arrange: No special setup needed

    # Act: Make POST request to signup for an activity with email as query param
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})

    # Assert: Should return 200 and success message
    assert response.status_code == 200
    assert "Signed up test@example.com for Chess Club" == response.json()["message"]


def test_signup_duplicate():
    # Arrange: Sign up once first
    client.post("/activities/Programming Class/signup", params={"email": "dup@example.com"})

    # Act: Try to sign up again
    response = client.post("/activities/Programming Class/signup", params={"email": "dup@example.com"})

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    assert "Student already signed up for this activity" == response.json()["detail"]


def test_signup_nonexistent_activity():
    # Arrange: No special setup needed

    # Act: Try to sign up for non-existent activity
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "test@example.com"})

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    assert "Activity not found" == response.json()["detail"]