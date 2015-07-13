#
#	RobotReviewer server
#

import os, logging
from flask import Flask, json
from flask import redirect, url_for, jsonify
from flask import request
from biasrobot import BiasRobot

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

DEBUG_MODE = str2bool(os.environ.get("DEBUG", "true"))
LOG_LEVEL = (logging.DEBUG if DEBUG_MODE else logging.INFO)
logging.basicConfig(level=LOG_LEVEL, format='[%(levelname)s] %(name)s %(asctime)s: %(message)s')
log = logging.getLogger(__name__)

app = Flask(__name__,  static_url_path='')
app.debug = DEBUG_MODE

log.info("loading models")
BOT = BiasRobot()
log.info("done loading models")

@app.route('/')
def main():
    return redirect(url_for('static',filename='index.html'))

@app.route('/annotate', methods = ['POST'])
def annotate():
    json_data = request.json
    annotations = BOT.annotate(json_data["text"])
    return json.dumps(annotations)

if __name__ == '__main__':
    app.run()
