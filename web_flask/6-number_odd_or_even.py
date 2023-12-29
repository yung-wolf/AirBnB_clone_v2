#!/usr/bin/python3

"""
module: 6-number_odd_or_even

A script that starts a Flask web application
"""

from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello():
    """Say Hello to HBNB."""
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Show HBNB."""
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def show_c(text):
    """Show C <text>."""
    return f"C {escape(text).replace('_', ' ')}"

@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def show_py(text='is cool'):
    """Show Python <text>."""
    return f"Python {escape(text).replace('_', ' ')}"

@app.route("/number/<int:n>", strict_slashes=False)
def show_num(n):
    """Show <n> if int."""
    return f"{n} is a number"

@app.route("/number_template/<int:n>", strict_slashes=False)
def show_num_template(n):
    """Show <n> template if int."""
    return render_template('5-number.html', num=n)

@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def is_num_odd_even(n):
    """Show if <n> is odd/even template if int."""
    return render_template('6-number_odd_or_even.html', num=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
