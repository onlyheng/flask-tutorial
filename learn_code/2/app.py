from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello():
    return '<center><h1>welcome to My WatchList</h1><img src="http://helloflask.com/totoro.gif"></center>'


@app.route('/user/<name>')
def user_usage(name):
    return f'User: {escape(name)}'


if __name__ == '__main__':
    app.run(debug=True)

