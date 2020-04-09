from flask import Flask,render_template, request, make_response, jsonify
import spacy
import sys


sys.path.append("/home/art/Downloads/code_g/skyeng-grammar-filter/nlp/processing")
import text_processor as tp
import pos_tagging
import active_voice
import passive_voice
# sys.path.append("/home/art/Downloads/code/skyeng-grammar-filter/nlp/processing")

nlp_pos = tp.nlp_setup(spacy.load('en_core_web_sm'), 'pos')
nlp_task_creator = tp.nlp_setup(spacy.load('en_core_web_sm'), 'tense')

app = Flask(__name__)
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/process', methods=["POST"])
def process():
	## JSON Request
	req = request.get_json()
	text = req["text"]
	task_type = req["taskType"]
	task_params = req["taskParams"]
# 	tense = req["tense"]
	## JSON ENDS

	active_result = []
	passive_result = []
	pos_result = []

	if task_type == "POS":
		pos_result = pos_tagging.pos_tag_search(nlp_pos, text, task_params)

	if task_type == 'ACTIVE':
		active_result = active_voice.active_voice_search_batches(nlp_task_creator, text, task_params)

	if task_type == 'PASSIVE':
		passive_result = passive_voice.passive_voice_search_batches(nlp_task_creator, text, task_params)

	res = make_response(jsonify(pos_result=pos_result, passive_result=passive_result, active_result=active_result), 200)
	return res

@app.route('/docs')
def docs():
	return render_template("docs.html")


if __name__ == '__main__':
	app.run(debug=True)
