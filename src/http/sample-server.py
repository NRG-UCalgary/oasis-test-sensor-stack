import flask

app = flask.Flask(__name__)
app.config['DEBUG']

@app.route('/', methods=['POST'])
def something():
    return 'ok!'

app.run(host='0.0.0.0', port='8888')
