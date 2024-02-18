#!/usr/bin/python3
"""HBNB Flask application."""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """
    Close the database connection after each request.

    Args:
        exception: Any exception that occurred during the request handling.
    """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Render a template to display a list of states."""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
