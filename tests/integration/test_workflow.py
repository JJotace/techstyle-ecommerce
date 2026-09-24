import pytest
from app import app

@pytest.fixture
def mock_db(mocker):
    """Mock database connection"""
    mock = mocker.MagicMock()

    def mock_execute(query, args=()):
        cursor = mocker.MagicMock()
        if "SELECT * FROM users WHERE username" in query:
            cursor.fetchall.return_value = []
        else:
            cursor.fetchall.return_value = []
        return cursor

    mock.execute.side_effect = mock_execute
    mocker.patch("app.get_db", return_value=mock)
    return mock

@pytest.fixture
def client(mock_db):
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_user_registration_flow(client):
    """Test complete user registration workflow"""
    rv = client.post("/register")
    assert rv.status_code == 200

    rv = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    assert rv.status_code in [200, 302]
