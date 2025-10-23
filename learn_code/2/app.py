from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "welcome to My WatchList"


if __name__ == '__main__':
    hello()

