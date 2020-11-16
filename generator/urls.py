from flask import Flask, Response
from generator.controllers import get_data

app = Flask(__name__)


@app.route('/')
def index():
    return Response(get_data(), mimetype="text/html")
