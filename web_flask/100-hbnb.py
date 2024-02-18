#!/usr/bin/python3
"""HBNBFlask application."""

from flask import Flask, render_template, Markup
from models import storage

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def states_cities_list():
    """Display a list of states and cities along with amenities and places."""
    states = list(storage.all("State").values())
    states.sort(key=lambda x: x.name)
    for state in states:
        state.cities.sort(key=lambda x: x.name)
    amenities = list(storage.all("Amenity").values())
    amenities.sort(key=lambda x: x.name)
    places = list(storage.all("Place").values())
    places.sort(key=lambda x: x.name)
    for place in places:
        place.description = Markup(place.description)
    return render_template(
        "100-hbnb.html", states=states, amenities=amenities, places=places
    )


@app.teardown_appcontext
def teardown_db(exception):
    """
    Close the database connection after each request.

    Args:
        exception: Any exception that occurred during the request handling.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
