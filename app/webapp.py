import json
import os

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask.json import JSONEncoder
from flask_socketio import SocketIO, emit

from skep.docker.swarm import Swarm

class DelegatingJSONEncoder(JSONEncoder):
    def default(self, obj):
        return self.serialize(obj)

    def serialize(self, obj):
        if isinstance(obj, dict):
            return dict((k, self.serialize(v)) for k, v in obj)
        if isinstance(obj, list):
            return [self.serialize(x) for x in obj]
        try:
            return obj.serializable()
        except AttributeError:
            return obj

application = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'templates'
    )
)

application.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key')
application.json_encoder = DelegatingJSONEncoder
socketio = SocketIO(application)

SECRET = os.environ.get('SKEP_SECRET', None)

@application.route('/files/<path:path>')
def files(path):
    return send_from_directory('files', path)

@application.route("/")
def root():
    return render_template(
        'layout.html',
        env=os.environ.get('SKEP_ENV', 'production'),
        css_md5=os.environ.get('CSS_MD5', ''),
        js_md5=os.environ.get('JS_MD5', '')
    )

@application.route("/swarm.json")
def swarm():
    return jsonify(Swarm().manifest())

@application.route("/stats", methods=["POST"])
def stats_create():
    if authorize_request(request, SECRET):
        socketio.emit("stats", json.dumps(request.get_json()), broadcast=True)
        return 'OK', 200
    return 'Unauthorized', 401

@socketio.on("manifest")
def handle_message():
    emit("manifest", json.dumps(Swarm().manifest(), cls=DelegatingJSONEncoder))

def authorize_request(request, secret):
    if secret is None:
        return True
    token = 'Token ' + secret
    if token == request.headers.get('Authorization', None):
        return True
    return False

if __name__ == "__main__":
    socketio.run(application, host=os.environ.get('SKEP_LISTEN_HOST', '127.0.0.1'))
