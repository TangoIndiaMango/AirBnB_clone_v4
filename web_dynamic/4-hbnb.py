#!/usr/bin/python3
""" Flash AirBnB Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Destroy current SQLAlchemy Session """
    storage.close()


@app.route('/4-hbnb', strict_slashes=False)
def hbnb():
    """ HBNB main function """
    states = storage.all(State).values()
    states = sorted(states, key=lambda st: st.name)
    st_data = []

    for state in states:
        st_data.append([state, sorted(state.cities, key=lambda c: c.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda a: a.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda p: p.name)

    return render_template('4-hbnb.html',
                           states=st_data,
                           amenities=amenities,
                           places=places, cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
