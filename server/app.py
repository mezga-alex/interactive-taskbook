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

sys.path.append(arch_home)
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

"""
"statistics": [{
        "article_links": [{
            "url": "",
            "exercise": [{
                "type": "",
                "words": [{
                    "value": "",
                    "correct": 0,
                    "wrong": 0,
                    "pos": "",
                }],
            }],
        }],
    }],
    
sample_user = {"user": "arch",
               "124tgfvsc": {
                   "article_links": {
                       "sample_com":
                           {
                               # "url": "sample.com",
                               # "exercise": {
                               "passive_all":
                                   {
                                       # "type": "passive_all",
                                       "words": {
                                           "1": {
                                               "value": "bruh",
                                               "correct": 1,
                                               "wrong": 14,
                                               "pos": "adj",
                                           },
                                           "2": {
                                               "value": "Sanya",
                                               "correct": 1,
                                               "wrong": 6,
                                               "pos": "noun",
                                           },
                                       },

                                   },
                           },
                       # },
                   },
               },
               }
"""

sample_user = {
    "session_id": "iiimfbnmnldgfepajlnghaccejcaiaik",
    "statistics": [],
}

# session_0 = {
#             "sample_com":
#                 {
#                     "passive_all":
#                         {
#                             "words": {
#                                 "1": {
#                                     "value": "bruh",
#                                     "correct": 1,
#                                     "wrong": 14,
#                                     "pos": "adj",
#                                 },
#                                 "2": {
#                                     "value": "Sanya",
#                                     "correct": 1,
#                                     "wrong": 6,
#                                     "pos": "noun",
#                                 },
#                             },
#
#                         },
#                 },
#             }


# active = {
#              "article_links": {
#                  "sample_com":
#                      {
#                          # "url": "sample.com",
#                          # "exercise": {
#                          "pos_all":
#                              {
#                                  # "type": "passive_all",
#                                  "words": {
#                                      "1": {
#                                          "value": "bruh",
#                                          "correct": 1,
#                                          "wrong": 14,
#                                          "pos": "adj",
#                                      },
#                                      "2": {
#                                          "value": "Sanya",
#                                          "correct": 1,
#                                          "wrong": 6,
#                                          "pos": "noun",
#                                      },
#                                  },
#
#                              },
#                      },
#                  # },
#              },
#          },

active_all = {
                 # "type": "passive_all",
                 "words": {
                     "1": {
                         "value": "bruh",
                         "correct": 1,
                         "wrong": 14,
                         "pos": "adj",
                     },
                     "2": {
                         "value": "Sanya",
                         "correct": 1,
                         "wrong": 6,
                         "pos": "noun",
                     },
                 },
             },

active_all_0 = {
                   # "type": "passive_all",
                   "words": {
                       "1": {
                           "value": "rgdfvh",
                           "correct": 1,
                           "wrong": 14,
                           "pos": "adj",
                       },
                       "2": {
                           "value": "Sasdfsdfya",
                           "correct": 1,
                           "wrong": 6,
                           "pos": "noun",
                       },
                   },
               },


# @app.route("/add_user", methods=["POST"])
# def add_user():
#     try:
#         # req = request.get_json()
#         # print(req)
#         collection.insert(active_all)
#     except request.exceptions as e:
#         print('request error occured: ', e)
#         return make_response(jsonify(result=[e]), 500)


@app.route('/update', methods=["POST"])
def update_user():
    try:
        req = request.get_json()
        print(req)
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


def insert_db():
    collection.insert_one(sample_user)


def update_db(session_id, stats):
    results = collection.find("session_id")
    sample_user = {
        "session_id": "iiimfbnmnldgfepajlnghaccejcaiaik",
        "statistics": [],
    }
    for result in results:
        print(result)
    # collection.update_one({"user": "arch"}, {"$set": {".".join([session, links, site, exercise]): active_all}})
    collection.update_one({"session_id": session_id}, {"$push": {"statistics": stats}})

    # collection.update_one({"user":"arch"}, {"$set": {session+"."+links+"."+site+"."+exercise: active_all}})
    # collection.update_one({"user": "arch"}, {"$set": {session: active}})


# /{"article_links": "sample_com"}

if __name__ == '__main__':
    insert_db()
    update_db()
    print('inserted')
    app.run(host='0.0.0.0', port=8050)
