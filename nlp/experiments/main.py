import pos_tagging
import passive_voice

from experiments.globals import Passive

if __name__ == "__main__":
    # parse.parse_data('test', path)
    # path = './created_files/sents_exp.txt'
    # path = './dataset/nyt_text.txt'
    # text = text_processor.lexical_processor(open(path).read().lower())

    task = 'passive_voice'
    tense = 'ALL'
    pos = 'VBN'
    text = Passive
    if task == 'pos':
        pos_tagging.pos_tag_search(pos, text)

    if task == 'passive_voice':
        passive_phrases = passive_voice.passive_voice_search(text, tense)

        file_passive_tree = open('./created_files/passive_voice_tree.txt', 'w')
        for phr in passive_phrases:
            file_passive_tree.write(phr + "\n")
        file_passive_tree.close()
