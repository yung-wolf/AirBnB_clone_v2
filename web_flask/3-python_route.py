#!/usr/bin/python3

"""
module: 3-python_route

A script that starts a Flask web application
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello():
    """Say hello to HBNB."""
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Show HBNB."""
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def show_c(text):
    """Display C <text>"""
    return f"C {escape(text).replace('_', ' ')}"

@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def show_py(text="is cool"):
    """Display Python <text>. Default value for text = `is cool`."""
    return f"Python {escape(text).replace('_', ' ')}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
