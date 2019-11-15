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