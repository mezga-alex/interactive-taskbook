from flask import Flask,render_template, request, make_response, jsonify
import spacy
import sys
import pos_tagging
import active_voice
import passive_voice

sys.path.append("/home/art/Downloads/code/skyeng-grammar-filter/nlp/processing")


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
	tense = req["tense"] 
	## JSON ENDS

	active_result = []
	passive_result = []
	pos_result = []

	if pos != "NONE":
		pos_result = pos_tagging.pos_tag_search(text, pos)

	if tense != 'NONE':
		active_result = active_voice.active_voice_search_batches(text, tense)

	if passive_voice_tense != 'NONE':
		passive_result = passive_voice.passive_voice_search_batches(text, passive_voice_tense)

	res = make_response(jsonify(pos_result=pos_result, passive_result=passive_result, active_result=active_result), 200)

	return res

@app.route('/docs')
def docs():
	return render_template("docs.html")


if __name__ == '__main__':
	app.run(debug=True)
