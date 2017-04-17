# -*- coding: UTF-8 -*-
from flask import Flask
from flask import render_template

import config
import composer
import filesystem

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('_/html.html')

@app.route('/<namespace>/<path:path>')
def render():
    return render_template('_/html.html')



filesystem.find("Авторская сеть")
# if __name__ == "__main__":
#     app.run(debug=True)
