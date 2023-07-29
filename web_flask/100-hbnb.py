#!/usr/bin/python3
"""Make the filters dynamic
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def close_session(ctx):
    """Closes the current session
    """
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays the HBNB main page
    """
    from models.amenity import Amenity
    from models.place import Place
    from models.state import State

    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template('100-hbnb.html', states=states,
                            amenities=amenities, places=places)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
