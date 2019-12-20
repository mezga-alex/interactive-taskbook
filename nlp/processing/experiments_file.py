import spacy
from spacy import displacy

import time
import text_processor

####### CHECK PARSING SPEED #######
path = '../created_files/sents_exp.txt'
path = '../dataset/nyt_text.txt'
text_plain = open(path).read().lower()
text_lines = open(path).readlines()
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 1500000

# start_time = time.time()
# doc = nlp(text_plain)
# elapsed_time = time.time() - start_time
# print("plain text: ", elapsed_time)
# print(sum(1 for i in doc.sents))

# start_time = time.time()
# docs = nlp.pipe(text_plain)
# elapsed_time = time.time() - start_time
# print("plain text pipe: ", elapsed_time)
# for doc in docs:
#     for sent in doc.sents:
#         print(sent)


# start_time = time.time()
# doc = [nlp(text) for text in text_lines]
# elapsed_time = time.time() - start_time
# print("plain-line text: ", elapsed_time)
# print(sum(1 for i in doc.sents))
#
# start_time = time.time()
# doc = list(nlp.pipe(text_lines))
# elapsed_time = time.time() - start_time
# print("batches text: ", elapsed_time)
# print(sum(1 for i in doc.sents))

text = "Dishes may be used, but they must not be left dirty in the sink.\
        The walls aren't painted by my mother.\
       My shoes should have been repaired last week."


doc = nlp(text)
displacy.serve(doc, style="dep")

