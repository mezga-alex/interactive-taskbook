###########################
#  Draft for experiments  #
###########################

import spacy


def set_custom_boundaries(doc):
    # Adds support to use `...` as the delimiter for sentence detection
    for token in doc[:-1]:
        if token.text == '...':
            doc[token.i + 1].is_sent_start = True
    return doc


# Too bad implementation
def create_train_data(text_file_dir, pos_file_dir):
    text = open(text_file_dir).read()
    pos = open(pos_file_dir).read()

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(set_custom_boundaries, before='parser')
    nlp.max_length = 1200000

    # Line-by-line sentences file
    doc = nlp(text)
    sentences = list(doc.sents)
    file_sent = open('./created_files/sents_train.txt', 'w')
    for sent in sentences:
        sent_str = str(sent)
        dot_end = sent_str.endswith(('.', '...', '?'))

        if dot_end:
            file_sent.write(sent_str + '\n')
        else:
            file_sent.write(sent_str + ' ')

    file_sent.close()


    # Line-by-line POS file
    doc = nlp(pos)
    pos_per_sents = list(doc.sents)

    file_sent = open('./created_files/pos_train.txt', 'w')
    for pos_sent in pos_per_sents:
        pos_sent_str = str(pos_sent)
        dot_end = pos_sent_str.endswith(('.', '...', '?'))

        if dot_end:
            file_sent.write(pos_sent_str + '\n')
        else:
            file_sent.write(pos_sent_str + ' ')
    file_sent.close()


# Convert parsed data for train
# Example:
# TRAIN_DATA = [
#     ("I like green eggs", {"tags": ["N", "V", "J", "N"]}),
#     ("Eat blue ham", {"tags": ["V", "J", "N"]}),
# ]
TRAIN_DATA = []


def init_train_data(pos_train_file_path=None, sents_train_file_path=None):
    if pos_train_file_path and sents_train_file_path:
        with open(sents_train_file_path) as sents_file, open(pos_train_file_path) as pos_file:
            for sent, pos in zip(sents_file, pos_file):
                sent = sent.strip()
                pos = pos.strip()

                TRAIN_DATA.append((sent, {"tags": pos.split()}))
    else:
        print('Incorrect paths')


init_train_data('./created_files/pos_exp', './created_files/sents_exp')
print(TRAIN_DATA)
