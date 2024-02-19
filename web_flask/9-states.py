#!/usr/bin/python3
"""HBNBFlask application."""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Route handler for displaying information about states."""
    states = storage.all(State)
    return render_template("9-states.html", states=states)


@app.route("/states/<state_id>", strict_slashes=False)
def state_id(state_id=None):
    """
    Route handler for displaying information about a specific state.

    Args:
        state_id (str, optional): The ID of the specific state.
    """
    states = storage.all(State)
    if state_id is not None:
        state_id = "State." + state_id
    return render_template("9-states.html", states=states, id=state_id)


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
