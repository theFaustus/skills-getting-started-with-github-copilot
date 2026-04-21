"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_all_activities(client):
    """Test retrieving all available activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == 3
    for activity_name in expected_activities:
        assert activity_name in data
        assert "description" in data[activity_name]
        assert "participants" in data[activity_name]
        assert "max_participants" in data[activity_name]


def test_activities_have_correct_structure(client):
    """Test that each activity has the required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    # Assert
    assert response.status_code == 200
    for field in required_fields:
        assert field in activity


def test_activities_participants_list(client):
    """Test that participants are correctly returned in activities"""
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert data["Chess Club"]["participants"] == expected_chess_participants
