#!/usr/bin/python3

"""
module: 1-hbnb_route.py

A script that starts a Flask web application
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """Say hello to HBNB."""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Show HBNB."""
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
