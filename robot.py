#
#	RobotReviewer server
#

from flask import Flask, json
app = Flask(__name__)


@app.route('/annotate', methods = ['POST'])
def annotate():
	json_data = request.json
	# do something to the json here...
	return json.dumps(json_data)

if __name__ == '__main__':
    app.run(debug=True)