#!/usr/bin/python3
"""HBNB Flask application."""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Display a list of cities grouped by states."""
    states = storage.all("State").values()
    return render_template("8-cities_by_states.html", states=states)


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