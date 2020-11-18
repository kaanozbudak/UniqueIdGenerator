from flask import Flask, Response, request, render_template
from generator.controllers import get_data

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return Response(
            "<form action='/' method='post'><input type='submit' value='Submit for start watching"
            "'/></form>", mimetype="text/html")
    elif request.method == 'POST':
        return Response(get_data(), mimetype="text/html")
    else:
        print('method not allowed')
        return 'method not allowed'
