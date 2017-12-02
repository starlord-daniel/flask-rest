from flask import Flask, jsonify, abort, request, make_response, url_for
from api import api

wsgi_app = api.wsgi_app

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 5555
    api.run(HOST, PORT)