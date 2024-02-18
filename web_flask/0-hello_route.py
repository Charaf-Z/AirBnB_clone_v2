#!/use/bin/python3
"""A simple Flask application to greet users with 'Hello HBNB!'."""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello() -> str:
    """
    Greet users with 'Hello HBNB!'.

    Returns:
        str: A greeting message.
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
