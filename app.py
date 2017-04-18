# -*- coding: UTF-8 -*-
import sys; reload(sys); sys.setdefaultencoding('utf-8');  reload(sys);
import sys;

from flask import Flask
from flask import render_template

import config
import composer
import filesystem
from pprint import pprint
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('_/html.html')

@app.route('/~<namespace>/<path:path>')
def render(namespace, path):
    path = path.split("/")
    publish_path = namespace
    if len(path) > 1:
        publish_path += "/"+path[0:-1]
    publish_tag  = path[-1]
    source = filesystem.find(publish_path, [publish_tag], config.filesystem.sources)
    return render_template('text.html', fragments=source)


# print filesystem.find('~textnet', [u"Авторская сеть"], config.filesystem.sources)


if __name__ == "__main__":
    app.run(debug=True)
