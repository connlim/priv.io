import json

from flask import Flask, request, send_from_directory, render_template
from test import extract

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route('/parse-tos', methods=['POST'])
def parse_tos():
    text = request.form.getlist('tos')[0]
    print(text)
    # return json.dumps(extract(text))
    return render_template('tos.html', tos=extract(text))


if __name__ == '__main__':
    app.run(debug=True)