#!/usr/bin/python3
"""HBNBFlask application."""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def filters():
    """Render a template to display filters for searching listings."""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template(
        "10-hbnb_filters.html", states=states, amenities=amenities
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
    app.run(host="0.0.0.0", port="5000")
