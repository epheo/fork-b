#!/usr/bin/env python
# -*- coding: utf-8 -*-

import data
import vincent
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

WIDTH = 600
HEIGHT = 300

@app.route("/data/stocks")
def stocks():
    line = vincent.Line(data.price[['HPQ']], width=WIDTH, height=HEIGHT)
    line.axis_titles(x='Date', y='Price')
    line.legend(title='Hewlett Packard Stock Price')
    return line.to_json()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
