#!/usr/bin/python3
"""Displays a list of cities in a specific state or all states.
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def close_session(ctx):
    """Closes the current session
    """
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Displays a list of cities in a specific state or all states
    """
    from models.state import State

    states = storage.all(State)
    if id is not None:
        id = 'State.' + id
    return render_template('9-states.html', states=states, id=id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
