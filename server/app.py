from flask import Flask, render_template, request, make_response, jsonify
import spacy
import sys
import pymongo

# init db
from pymongo import MongoClient
import datetime

cluster = MongoClient("mongodb+srv://arch:lbpfqycfrctc@itb-xeeen.mongodb.net/test?retryWrites=true&w=majority")
arch_home = '/home/art/Downloads/code_g/skyeng-grammar-filter/nlp/processing'
arch_work = "/home/art/Downloads/pipe/skyeng-grammar-filter/nlp/processing"

sys.path.append(arch_work)
import text_processor as tp
import pos_tagging
import active_voice
import passive_voice

spacy.prefer_gpu()
print(spacy.prefer_gpu())
nlp_pos = tp.nlp_setup(spacy.load('en_core_web_sm'), 'pos')
nlp_task_creator = tp.nlp_setup(spacy.load('en_core_web_sm'), 'tense')

app = Flask(__name__)
db = cluster.itb
collection = db.users


sample_user = {
    "session_id": "iiimfbnmnldgfepajlnghaccejcaiaik",
    "statistics": [],
}


@app.route('/get_db', methods=["GET", "POST"])
def get_user():
    try:
        # connect to json

        req = request.get_json()
        print(req)
        return make_response(jsonify(200))
    except request.exceptions as e:
        print('request error occured: ', e)
        return make_response(jsonify(result=[e]), 500)


@app.route('/update', methods=["POST"])
def update_user():
    try:
        req = request.get_json()
        # print(req)
        session_id = req['extensionID']
        _json = req['json']
        stats = _json['statistics']
        print(session_id)
        print(stats)
        update_db(session_id, stats)
        return make_response(jsonify(200))
    except request.exceptions as e:
        print('request error occured: ', e)
        return make_response(jsonify(result=[e]), 500)


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


def add_user(session_id):
    sample_user = {
        "session_id": session_id,
        "statistics": [],
    }
    collection.insert_one(sample_user)


def update_db(session_id, stats):
    results = list(collection.find({"session_id": session_id}))
    print("result", type(results))
    # print(results[0])

    if len(results) == 0:
        add_user(session_id)

    collection.update_one({"session_id": session_id}, {"$push": {"statistics": stats}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
