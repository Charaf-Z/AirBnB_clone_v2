#!/use/bin/python3
"""A simple Flask application to greet users with 'Hello HBNB!'."""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB!"


app.run(host="0.0.0.0", port="5000")
