from flask import Flask, Response
from generator.controllers import generator

app = Flask(__name__)


@app.route('/')
def index():
    return Response(generator(), mimetype='text/event-stream')
