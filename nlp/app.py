from flask import Flask,render_template, request, make_response, jsonify
import spacy
import sys
import text_processor as tp
import pos_tagging
import active_voice
import passive_voice

sys.path.append("/home/art/Downloads/pipe/skyeng-grammar-filter/nlp/processing")

spacy.prefer_gpu()
print(spacy.prefer_gpu())
nlp_pos = tp.nlp_setup(spacy.load('en_core_web_sm'), 'pos')
nlp_task_creator = tp.nlp_setup(spacy.load('en_core_web_sm'), 'tense')

app = Flask(__name__)


@app.route('/', methods=["POST"])
def process():
	# JSON Request
	try:
		result = []
		req = request.get_json()
		text = req["text"]
		task = req["task"]
		specified_task = req["specifiedTask"]
		# JSON ENDS

		if task == "POS":
			result = pos_tagging.pos_tag_search(nlp_pos, text, specified_task)

		if task == 'ACTIVE_VOICE':
			result = active_voice.active_voice_search_batches(nlp_task_creator, text, specified_task)

		if task == 'PASSIVE_VOICE':
			result = passive_voice.passive_voice_search_batches(nlp_task_creator, text, specified_task)

		return make_response(jsonify(result=result), 200)
	except request.exceptions as e:
		print('request error occured: ', e)
		return make_response(jsonify(result=[e]), 500)


@app.route('/answer', methods=["POST"])
def answer():
	## JSON Request
	req = request.get_json()
	text = req["text"]
	print("html", req["pos"])
	results = req["result"]
	return render_template("index.html", results=results, num_of_results=len(results), text=text)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8050)
