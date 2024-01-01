#!/usr/bin/python3

"""
module: 7-states_list

A script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def rem_session(exception):
    '''Remove current SQLAlchemy Session.'''
    storage.close()


@app.route("/states_list", strict_slashes=False)
def list_states():
    '''List all State objects from storage.'''
    states = storage.all(State).values()
    sort_states = sorted(states, key=lambda x: x.name)
    return render_template("7-states_list.html", states=sort_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
