#!/usr/bin/env python3

"""Bare Flask App"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Wine Catalog goes here"

if __name__ == '__main__':
    app.run()