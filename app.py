from flask import Flask
from flask import request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'test1'


if __name__ == '__main__':
    app.debug=True
    app.run()
