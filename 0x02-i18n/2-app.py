#!/usr/bin/env python3
'''This is the Flask module
'''

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    '''this is the class of config'''

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """this gets the locale for a web page.

    Returns:
        str: best match
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''this is the route

    Returns:
        html: homepage
    '''
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
