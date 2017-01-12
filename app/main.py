import sqlite3
from flask import Flask


app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('pokemondata.db')


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
