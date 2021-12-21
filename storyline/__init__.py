from flask import (
    Flask,
    request,
)
from json import dumps
from pathlib import Path
from subprocess import run


def type_of_dir(dir_path):
    if (dir_path / '.git').exists():
        return "worktree"
    else:
        git_process = run(["git", "rev-parse", "--git-dir"], cwd=dir_path)
        if git_process.returncode == 0:
            return "bare"
        return "directory"


def create_app():
    app = Flask('Storyline')

    @app.route('/api/dirs', defaults={'path': None})
    @app.route('/api/dirs/<path:path>')
    def dirs(path):
        if path is None:
            path = Path.home()

        p = Path(f'/{path}')
        directories = [child for child in p.iterdir() if child.is_dir()]

        results = []
        for dir in directories:
            if (dir / '.git').exists:
                results.append({
                    'name': dir.name,
                    'type': type_of_dir(dir),
                })

        return dumps(results)

    
    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    def catch_all_statics(path):
        return app.send_static_file(path)

    return app