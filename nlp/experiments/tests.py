import text_processor
import pos_tagging
import passive_voice as pv
import time
import passive_voice_cython
import spacy

from experiments.globals import Passive

if __name__ == "__main__":
    # path = './dataset/train.txt'
    # parse.parse_data('train', path)
    # path = './created_files/sents_exp.txt'
    # path = './created_files/sents_train.txt'
    path = './dataset/nyt_text_2.txt'
    text = text_processor.lexical_processor(open(path).read().lower())

    task = 'passive_voice'
    tense = 'ALL'
    pos = 'VBN'
    text = Passive
    # text = "I have a feeling that a secret may be being kept."
    if task == 'pos':
        pos_tagging.pos_tag_search(pos, text)

    if task == 'passive_voice':
        start_time = time.time()
        passive_phrases = pv.passive_voice_search(text, tense)
        elapsed_time = time.time() - start_time
        print("tree single:", elapsed_time)

        start_time = time.time()
        passive_phrases_batches = pv.passive_voice_search_batches(text, tense)
        elapsed_time = time.time() - start_time
        print("tree batches:", elapsed_time)

        start_time = time.time()
        passive_phrases_batches_exp = pv.passive_voice_search_exp(text, tense)
        elapsed_time = time.time() - start_time
        print("tree batches upd:", elapsed_time)

        start_time = time.time()
        passive_phrases_matcher = pv.matcher_passive_voice_search(text)
        elapsed_time = time.time() - start_time
        print("matcher batches:", elapsed_time)

    file_passive_tree = open('./created_files/passive_voice_tree.txt', 'w')
    file_passive_tree_batches = open('./created_files/passive_voice_tree_batches.txt', 'w')
    file_passive_tree_batches_exp = open('./created_files/passive_voice_tree_batches_exp.txt', 'w')
    file_passive_matcher = open('./created_files/passive_voice_matcher.txt', 'w')

    for phr in passive_phrases:
        file_passive_tree.write(phr + "\n")

    for phr in passive_phrases_batches:
        file_passive_tree_batches.write(phr + "\n")

    for phr in passive_phrases_batches_exp:
        file_passive_tree_batches_exp.write(phr + "\n")

    for phr in passive_phrases_matcher:
        file_passive_matcher.write(phr + "\n")

    file_passive_tree.close()
    file_passive_tree_batches.close()
    file_passive_tree_batches_exp.close()
    file_passive_matcher.close()

    nlp = spacy.load('en_core_web_sm')
    n = 1000
    text_splited = [text[i:i + n] for i in range(0, len(text), n)]
    docs = list(nlp.pipe(text_splited))
    passive_voice_cython.main_nlp_fast(docs)
