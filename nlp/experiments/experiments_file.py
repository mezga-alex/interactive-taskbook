import spacy
from spacy import displacy
import matplotlib.pyplot as plt
import time
import text_processor


# def batch_num_time_measurement(text, min_num_of_batches, max_num_of_batches):
#     time_arr = []
#     num_of_batches_arr = []
#
#     chars_processed = 0
#     while chars_processed < len()
#
#     for n in range(min_num_of_batches, max_num_of_batches):
#         batch_size = len(text) / n
#         division_remainder = len(text) % n
#
#         text_splited = [text_full[i:i + batch_size] for i in range(0, len(text_full), batch_size)]
#         start_time = time.time()
#         docs = list(nlp.pipe(text_splited))
#         elapsed_time = time.time() - start_time


def batch_length_time_measurement(text, min_batch, max_batch=0, step=100, trace=False):
    text_len = len(text)

    # Check the boundaries
    if min_batch > text_len:
        min_batch = text_len
    if max_batch > text_len:
        max_batch = text_len
    if max_batch == 0 or max_batch < min_batch:
        max_batch = min_batch

    # Outer loop for batch size
    time_arr = []
    size_arr = []
    batch_size = min_batch
    while batch_size <= max_batch:
        text_batches = []
        start_span = 0

        # Inner loop for a specific size
        while start_span < text_len:
            end_span = start_span + batch_size
            # Check the out of range
            if end_span > text_len:
                end_span = text_len

            batch = text[start_span:end_span]
            text_batches.append(batch)

            start_span = end_span
        start_time = time.time()
        docs = list(nlp.pipe(text_batches))
        elapsed_time = time.time() - start_time

        time_arr.append(elapsed_time)

        size_arr.append(batch_size)

        if trace:
            last_batch = text_batches[len(text_batches)-1]
            print("-"*30)
            print("Text length = ", text_len)
            print("Batch size = ", batch_size)
            print("Num of batches = ", len(text_batches))
            print("Last batch size = ", len(last_batch))
            print("Last batch:")
            print(last_batch + "\n")

        batch_size += step

    return time_arr, size_arr


####### CHECK PARSING SPEED #######
#path = '../created_files/sents_train.txt'
path = '../dataset/nyt_text.txt'
text_full = open(path).read()

nlp = spacy.load('en_core_web_sm')
nlp.max_length = 1500000

# start_time = time.time()
# doc = nlp(text_full)
# elapsed_time_plain = time.time() - start_time
# print("plain text: ", elapsed_time_plain)
# print(sum(1 for i in doc.sents))

# ######## PARSING WITH BATCHES ######
time, size = batch_length_time_measurement(text_full, 200, 5000, 200, True)
min_index = time.index(min(time))

fig = plt.figure()
plt.plot(size, time, label="divided into batches")
plt.scatter(size[min_index], time[min_index], s=15, c='red', label="minimum time")
plt.legend()
plt.xlabel('batch size', fontsize=16)
plt.ylabel('time', fontsize=16)
plt.title(str(len(text_full)) + " characters of text", fontsize=18)
fig.savefig('nyt_text_small_batches.png')
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
