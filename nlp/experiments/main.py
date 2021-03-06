import pos_tagging
import passive_voice
import passive_voice_exp
import displacy_file
from experiments.globals import Passive

if __name__ == "__main__":
    # parse.parse_data('test', path)
    path = './created_files/sents_exp.txt'
    # path = './dataset/nyt_text.txt'
    # text = text_processor.lexical_processor(open(path).read().lower())

    task = 'pos'
    tense = 'ALL'
    pos = 'ALL'
    text = Passive

    displacy_file.displacy_func(text)

    if task == 'pos':
        pos_tagging.pos_tag_search(text, pos)
    #
    # if task == 'passive_voice':
    #     passive_phrases = passive_voice_exp.passive_voice_search(text, tense)
    #
    #     file_passive_tree = open('./created_files/passive_voice_tree.txt', 'w')
    #     for phr in passive_phrases:
    #         file_passive_tree.write(phr + "\n")
    #     file_passive_tree.close()

