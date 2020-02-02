from flask import Flask,render_template,url_for,request, make_response, jsonify
# import re
# import pandas as pd
import spacy
# from spacy import displacy
# import en_core_web_sm
nlp = spacy.load('en_core_web_sm')
import sys
sys.path.append("/home/art/Downloads/code/skyeng-grammar-filter/nlp/processing")
# sys.path.append("/home/poltavsky/InteractiveTaskBook/processing")
import text_processor
import pos_tagging
import passive_voice
import time

from globals import Passive, Active
import parse


app = Flask(__name__)
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/process',methods=["POST"])
def process():
	## JSON Request
	req = request.get_json()
	print("text", req["text"])
	text = req["text"]
	_passive_voice = "all"
	if passive_voice != 'NONE':
		start_time = time.time()
		passive_result = passive_voice.passive_voice_search_batches(text)
		elapsed_time = time.time() - start_time
		print("tree batches:", elapsed_time)

		start_time = time.time()
		passive_result = passive_voice.passive_voice_search(text)
		elapsed_time = time.time() - start_time
		print("tree single:", elapsed_time)

	res = make_response(jsonify(result=passive_result), 200)
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
