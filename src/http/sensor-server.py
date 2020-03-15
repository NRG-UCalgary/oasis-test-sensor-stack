import flask
import os

server_port = os.environ["SERVER_PORT"]

app = flask.Flask(__name__)
app.config['DEBUG']

@app.route('/', methods=['POST'])
def something():
    return 'ok!'

app.run(host='0.0.0.0', port=server_port)

