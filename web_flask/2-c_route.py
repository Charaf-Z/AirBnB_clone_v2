#!/use/bin/python3
"""A simple Flask ."""
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


@app.route("/hbnb", strict_slashes=False)
def hbnb() -> str:
    """
    Return 'HBNB'.

    Returns:
        str: A message.
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text: str = None) -> str:
    """
    Route that displays 'C ' followed by the value of 'text'.

    Args:
        text (str): The input text.

    Returns:
        str: A formatted message.
    """
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
