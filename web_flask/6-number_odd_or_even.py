#!/usr/bin/python3
"""A simple Flask ."""
from flask import Flask, render_template

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


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text: str = "is cool") -> str:
    """
    Route that displays 'Python ' followed by the value of 'text'.

    Args:
        text (str): The input text.

    Returns:
        str: A formatted message.
    """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number(n: int):
    """
    Route that displays a message indicating the input is a number.

    Args:
        n (int): The input number.
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_templase(n: int):
    """
    Route that renders a template with the number passed as parameter.

    Args:
        n (int): The input number.
    """
    return render_template("5-number.html", number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even_template(n: int):
    """
    Route that renders a template to display whether a number is odd or even.

    Args:
        n (int): The input number.
    """
    return render_template(
        "6-number_odd_or_even.html",
        number=n,
        is_odd="odd" if n % 2 == 1 else "even",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
