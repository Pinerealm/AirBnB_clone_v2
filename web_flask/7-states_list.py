#!/usr/bin/python3
"""Displays a list of all State objects in the database
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def close_session(ctx):
    """Closes the current session
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a list of all State objects in the database, sorted by name
    """
    from models.state import State

    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
