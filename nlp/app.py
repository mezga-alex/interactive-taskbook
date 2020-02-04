from flask import Flask,render_template, request, make_response, jsonify
# import re
# import pandas as pd
import spacy
# from spacy import displacy
# import en_core_web_sm
nlp = spacy.load('en_core_web_sm')
import sys
# sys.path.append("/home/art/Desktop/code/skyeng-grammar-filter-master/skyeng-grammar-filter-master/nlp/processing")
sys.path.append("/home/poltavsky/InteractiveTaskBook/processing")
import pos_tagging
import passive_voice
import passive_voice_exp

import time

app = Flask(__name__)
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/process',methods=["POST"])
def process():
	## JSON Request
	req = request.get_json()
	# print(req["pos"])
	# print("text", req["text"])
	# print("passive", req["passive_voice"])
	text = req["text"]
	pos = req["pos"]
	_passive_voice = req["passive_voice"]
	tense = req["tense"]
	##JSON ENDS

	passive_result = []
	results = []

	if pos != "NONE":
		pos_tagging.pos_tag_search(text, pos)

	if passive_voice != 'NONE':
		start_time = time.time()
		passive_result = passive_voice.passive_voice_search_batches(text)
		elapsed_time = time.time() - start_time
		print("tree batches:", elapsed_time)

		# start_time = time.time()
		# passive_result = passive_voice_exp.passive_voice_search(text, _passive_voice)
		# elapsed_time = time.time() - start_time
		# print("tree single:", elapsed_time)

		# pos_tagging.pos_tag_search(text, "ALL")


# 	return render_template("index.html", results=results, num_of_results=len(results), text=text)
    # dict_url = {"url": "http://poltavsky.pythonanywhere.com/"}
# 	res = make_response(jsonify(dict_url), 200)
	url_gen = "http://poltavsky.pythonanywhere.com"
	res = make_response(jsonify(url=url_gen, result=passive_result), 200)

# 	answer(results, text)
	return res

@app.route('/answer',methods=["POST"])
def answer():
	## JSON Request
	req = request.get_json()
# 	print(req["result"])
	print("text", req["text"])
# 	print("passive", req["passive_voice"])
	text = req["text"]
	print("html", req["pos"])
	results = req["result"]
	return render_template("index.html", results=results, num_of_results=len(results), text=text)

# @app.route('/answer',methods=["POST"])
# def answer(results, text):
#     res = results
#     print(res)
# 	return render_template("index.html", results=results, num_of_results=len(results), text=text)



if __name__ == '__main__':
	app.run(debug=True)
