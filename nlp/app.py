from flask import Flask,render_template, request, make_response, jsonify
import spacy
import sys
import pos_tagging
import passive_voice

import time

sys.path.append("/home/art/Downloads/code/skyeng-grammar-filter/nlp/processing")
nlp = spacy.load('en_core_web_sm')


app = Flask(__name__)
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/process',methods=["POST"])
def process():
	## JSON Request
	req = request.get_json()
	text = req["text"]
	pos = req["pos"]
	passive_voice_tense = req["passive_voice"]
	tense = req["tense"]  # For the future
	##JSON ENDS

	passive_result = []
	pos_result = []

	if pos != "NONE":
		pos_result = pos_tagging.pos_tag_search(text, pos)

	if passive_voice_tense != 'NONE':
		passive_result = passive_voice.passive_voice_search_batches(text, passive_voice_tense)

	res = make_response(jsonify(pos_result=pos_result, passive_result=passive_result), 200)

	return res

@app.route('/answer',methods=["POST"])
def answer():
	## JSON Request
	req = request.get_json()
	text = req["text"]
	results = req["result"]
	return render_template("index.html", results=results, num_of_results=len(results), text=text)


if __name__ == '__main__':
	app.run(debug=True)
