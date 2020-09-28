#!/usr/bin/env python3

"""Bare Flask App With Database"""

import sys
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    p = sys.prefix
    return "<p>Wine Catalog goes here.</p>" % (p)

if __name__ == '__main__':
    app.run()