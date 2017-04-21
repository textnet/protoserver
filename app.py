# -*- coding: UTF-8 -*-
import sys; reload(sys); sys.setdefaultencoding('utf-8');  reload(sys);
import sys;

from flask import Flask
from flask import render_template
from flask import send_from_directory

import config
import filesystem
from pprint import pprint
import json
import render

app = Flask(__name__)

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('assets', path)

@app.route("/")
def hello():
    return render_template('_/html.html')

@app.route('/~<namespace>/<path:path>')
def content(namespace, path):
    path = path.split("/")
    publish_path = namespace
    if len(path) > 1:
        publish_path += "/"+path[0:-1]
    publish_tag  = path[-1]
    fragments = filesystem.find(publish_path, [publish_tag], config.filesystem.sources)
    return render_template('text.html', fragments=render.render_fragments(fragments))


# print filesystem.find('~textnet', [u"Авторская сеть"], config.filesystem.sources)


if __name__ == "__main__":
    app.run(debug=True)
