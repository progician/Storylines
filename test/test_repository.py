import pytest

from json import loads, dumps

from storyline import create_app

@pytest.fixture
def client():
    """Create and configure an instance of the application."""
    app = create_app()
    with app.test_client() as client:
        yield client


def test_repostory_list_is_empty_by_default(client):
    response = client.get('/api/repository')
    assert response.status_code == 200

    json_response = loads(response.data.decode('utf-8'))
    assert len(json_response) == 0
