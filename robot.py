#
#	RobotReviewer server
#

from flask import Flask, json
app = Flask(__name__)

from biasrobot import BiasRobot

print "Loading models...",
BOT = BiasRobot()
print "DONE!"

@app.route('/annotate', methods = ['POST'])
def annotate():
	json_data = request.json
	annotations = BOT.annotate(json_data["text"]) # just does randomization for now
	return json.dumps(annotations)

if __name__ == '__main__':
    app.run()