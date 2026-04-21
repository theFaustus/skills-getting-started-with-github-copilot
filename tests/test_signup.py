"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_signup_new_participant(client):
    """Test successful signup of a new participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"
    initial_count = 2  # emma and sophia
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    activities_response = client.get("/activities")
    data = activities_response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data[activity_name]["participants"]) == initial_count + 1
    assert email in data[activity_name]["participants"]


def test_signup_duplicate_participant_rejected(client):
    """Test that duplicate signup is rejected"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test signup for a non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_participants_in_same_activity(client):
    """Test that multiple different participants can sign up"""
    # Arrange
    activity_name = "Gym Class"
    emails = ["student1@mergington.edu", "student2@mergington.edu"]
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={emails[0]}"
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={emails[1]}"
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    activities_response = client.get("/activities")
    data = activities_response.json()
    for email in emails:
        assert email in data[activity_name]["participants"]
