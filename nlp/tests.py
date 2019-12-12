import text_processor
import pos_tagging
import passive_voice as pv
import time
import parse

from numba import double
from numba.decorators import jit, autojit

from globals import Passive, Active

if __name__ == "__main__":
    path = './dataset/train.txt'
    parse.parse_data('train', path)
    # path = './created_files/sents_exp.txt'
    # path = './dataset/nyt_text.txt'
    # text = text_processor.lexical_processor(open(path).read().lower())

    task = 'passive_voice'
    tense = 'PAST_SIMPLE'
    pos = 'VBN'
    text = Passive
    if task == 'pos':
        pos_tagging.pos_tag_search(pos, text)

    if task == 'passive_voice':
        start_time = time.time()
        passive_phrases = pv.passive_voice_search(text, tense)
        elapsed_time = time.time() - start_time
        print("tree single:", elapsed_time)

        # pairwise_numba = autojit(pv.passive_voice_search)
        # start_time = time.time()
        # passive_phrases_numba = pairwise_numba(text, tense)
        # elapsed_time = time.time() - start_time
        # print("tree numba:", elapsed_time)


        start_time = time.time()
        passive_phrases_matcher = pv.matcher_passive_voice_search(text)
        elapsed_time = time.time() - start_time
        print("matcher:", elapsed_time)

    file_passive_tree = open('./created_files/passive_voice_tree.txt', 'w')
    # file_passive_phrases_numba = open('./created_files/passive_voice_tree_numba.txt', 'w')
    file_passive_matcher = open('./created_files/passive_voice_matcher.txt', 'w')

    for phr in passive_phrases:
        file_passive_tree.write(phr + "\n")

    # for phr in passive_phrases_numba:
    #     file_passive_phrases_numba.write(phr + "\n")

    for phr in passive_phrases_matcher:
        file_passive_matcher.write(phr + "\n")
    file_passive_tree.close()
    # file_passive_phrases_numba.close()
    file_passive_matcher.close()
