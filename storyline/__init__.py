from flask import Flask, request
from json import dumps

def create_app():
    app = Flask('Storyline')

    @app.route('/api/repository')
    def repository():
        if request.method == 'GET':
            return dumps([])

    return app