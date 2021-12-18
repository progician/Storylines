import pytest
from pytest_unordered import unordered

from json import loads, dumps

from storyline import create_app
from subprocess import run

@pytest.fixture
def client():
    """Create and configure an instance of the application."""
    app = create_app()
    with app.test_client() as client:
        yield client


def test_dir_query_only_list_directories_at_path(client, tmp_path):
    SOME_DIRECTORY = 'directory'
    d = tmp_path / SOME_DIRECTORY
    d.mkdir()
    f = tmp_path / 'file.txt'
    f.write_text('This file must not be shown in the API call.')

    api_request = f'/api/dirs{tmp_path}'
    print(api_request)
    directories = loads(client.get(api_request).data.decode('utf-8'))
    assert directories == [{'name': SOME_DIRECTORY, 'type': 'directory'}]


def test_dir_query_marks_repositories(client, tmp_path):
    SOME_DIRECTORY = 'directory'
    plain_old_directory = tmp_path / SOME_DIRECTORY
    plain_old_directory.mkdir()

    SOME_REPOSITORY = 'repository'
    repository = tmp_path / 'repository'
    repository.mkdir()

    run(['git', 'init'], cwd=repository)


    api_request = f'/api/dirs{tmp_path}'
    print(api_request)
    directories = loads(client.get(api_request).data.decode('utf-8'))
    assert directories == unordered([
        {'name': SOME_DIRECTORY, 'type': 'directory'},
        {'name': SOME_REPOSITORY, 'type': 'worktree'},
    ])
