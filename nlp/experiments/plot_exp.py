import spacy
from spacy import displacy
import matplotlib.pyplot as plt
import time
import sys
import pandas as pd
import seaborn as sns
sys.path.append("/home/art/Downloads/pipe/skyeng-grammar-filter/nlp/processing")
import text_processor
import os


def time_measurement(text, nlp, min_batch, max_batch=0, step=100, trace=False):
    time_arr = []
    size_arr = []
    num_batches = []

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
        num_batches.append(len(text_batches))
        size_arr.append(batch_size)

        if trace:
            last_batch = text_batches[len(text_batches) - 1]
            print("-" * 30)
            print("Text length = ", text_len)
            print("Batch size = ", batch_size)
            print("Num of batches = ", len(text_batches))
            print("Last batch size = ", len(last_batch))
            print("Last batch:")
            print(last_batch + "\n")

        batch_size += step

    return [time_arr, size_arr, num_batches]


def plot_results(path_to_csv, plt_show=False):
    """
    plot results by provided path of csv file
    :param path_to_csv:
    :param plt_show: True for showing on IDE, False for better look in jupyter notebook
    :return:
    """
    df = pd.read_csv(path_to_csv, index_col="size")
    f, axes = plt.subplots(1, 1, figsize=(10, 10), sharex=True)
    f.canvas.set_window_title(path_to_csv)
    plt.title(path_to_csv)
    ax = sns.lineplot(x=df.index, y="time", data=df)
    f.savefig('./'+path_to_csv.split('.')[0]+'.png')
    if plt_show:
        plt.show()


def export_csv(result, param, continue_df):
    indexes = ['time', 'size', 'num_batch']

    path = param + '_batch_result.csv'
    if continue_df and os.path.exists(path):
        df_default = pd.read_csv(path)
        df = pd.DataFrame(list(zip(result[0], result[1], result[2])),
                          columns=indexes)
        df = pd.concat([df_default, df], axis=0)
        print(df.shape)
    else:
        print(result[0], result[1], result[2])
        df = pd.DataFrame(list(zip(result[0], result[1], result[2])),
                          columns=indexes)

    df.to_csv(path, index=False, index_label=None)
    return path


def parsing_no_batch(path, text_full):
    text_full = open(path).read().lower()
    text_lines = open(path).readlines()
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    start_time = time.time()
    doc = nlp(text_full)
    elapsed_time_plain = time.time() - start_time
    print("plain text: ", elapsed_time_plain)
    print(sum(1 for i in doc.sents))


def test_len_batch(path, num):
    # ######## PARSING WITH BATCHES ######
    text_full = open(path).read().lower()
    # text_lines = open(path).readlines()
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000
    for i in range(num):
        result = time_measurement(text_full, nlp, 100, 5000, 100)
        csv_path = export_csv(result, str(num)+"_len", continue_df=True)
    print("done: ", csv_path)
    plot_results(csv_path, True)


# def matplot(text_full):
#     time, size = time_measurement(text_full, 100, 5000, 100)
#     min_index = time.index(min(time))
#     fig = plt.figure()
#     plt.plot(size, time, label="divided into batches")
#     plt.scatter(size[min_index], time[min_index], s=15, c='red', label="minimum time")
#     plt.legend()
#     plt.xlabel('batch size', fontsize=16)
#     plt.ylabel('time', fontsize=16)
#     plt.title(str(len(text_full)) + " characters of text", fontsize=18)
#
#     fig.savefig('/home/art/Downloads/pipe/skyeng-grammar-filter/nlp/experiments/nyt_text_small_batches.png')
#     plt.show()


def main():
    path = '../dataset/nyt_text.txt'
    test_len_batch(path, 10)

    # example of showing existing csv
    # csv_path = '10_len_batch_result.csv'
    # plot_results(csv_path, True)


if __name__ == '__main__':
    main()




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
