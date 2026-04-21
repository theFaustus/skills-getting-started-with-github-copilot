"""Tests for GET / endpoint using AAA pattern"""


def test_root_redirect_to_index(client):
    """Test that root path redirects to static index.html"""
    # Arrange & Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows_to_static(client):
    """Test that following the redirect works"""
    # Arrange & Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
