"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""


def test_unregister_existing_participant(client):
    """Test successful unregistration of a participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister actually removes the participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    initial_count = 2  # michael and daniel
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    activities_response = client.get("/activities")
    data = activities_response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data[activity_name]["participants"]) == initial_count - 1
    assert email not in data[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_400(client):
    """Test unregistration of someone not registered"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    """Test unregistration from a non-existent activity"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_then_signup_again(client):
    """Test that a participant can unregister and then sign up again"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    activities_response = client.get("/activities")
    data = activities_response.json()
    assert email in data[activity_name]["participants"]
