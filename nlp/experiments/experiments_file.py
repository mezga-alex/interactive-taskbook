import spacy
from spacy import displacy
import matplotlib.pyplot as plt
import time
import text_processor


def time_measurement(min_batch, max_batch, step):
    time_arr = []
    size_arr = []
    for n in range(min_batch, max_batch, step):
        text_splited = [text_full[i:i + n] for i in range(0, len(text_full), n)]
        start_time = time.time()
        docs = list(nlp.pipe(text_splited))
        elapsed_time = time.time() - start_time
        print("batches: ", len(text_splited), " n = ", n, "elapsed_time = ", elapsed_time)

        time_arr.append(elapsed_time)
        size_arr.append(n)

    return time_arr, size_arr

####### CHECK PARSING SPEED #######
#path = '../created_files/sents_train.txt'
path = '../dataset/nyt_text.txt'
text_full = open(path).read().lower()
text_lines = open(path).readlines()
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 1500000

start_time = time.time()
doc = nlp(text_full)
elapsed_time_plain = time.time() - start_time
print("plain text: ", elapsed_time_plain)
print(sum(1 for i in doc.sents))

# ######## PARSING WITH BATCHES ######
time, size = time_measurement(100, 5000, 100)
min_index = time.index(min(time))

fig = plt.figure()
plt.plot(size, time, label="divided into batches")
plt.scatter(size[min_index], time[min_index], s=15, c='red', label="minimum time")
plt.legend()
plt.xlabel('batch size', fontsize=16)
plt.ylabel('time', fontsize=16)
plt.title(str(len(text_full)) + " characters of text", fontsize=18)
fig.savefig('./experiments/nyt_text_small_batches.png')
plt.show()

# sum_ = 0
# for doc in docs:
#     sum_ += sum(1 for i in doc.sents)
# print(sum_)

# text = "Dishes may be used, but they must not be left dirty in the sink.\
#         The walls aren't painted by my mother.\
#        My shoes should have been repaired last week."
#
#
# doc = nlp(text)
# displacy.serve(doc, style="dep")
#
