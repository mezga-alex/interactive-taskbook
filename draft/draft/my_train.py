from __future__ import unicode_literals, print_function

import parse

import plac
import random
from pathlib import Path
import spacy
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.matcher import Matcher
from spacy.util import minibatch, compounding


TRAIN_DATA = []


def init_train_data(pos_train_file_path=None, sents_train_file_path=None):
    if pos_train_file_path and sents_train_file_path:
        with open(sents_train_file_path) as sents_file, open(pos_train_file_path) as pos_file:
            for sent, pos in zip(sents_file, pos_file):
                sent = sent.strip()
                pos = pos.strip()
                if len(sent.split()) == len(pos.split()):
                    TRAIN_DATA.append((sent, {"tags": pos.split()}))

    else:
        print('Incorrect paths')


def main(lang="en", output_dir=None, n_iter=25):
    """Create a new model, set up the pipeline and train the tagger. In order to
    train the tagger with a custom tag map, we're creating a new Language
    instance with a custom vocab.
    """
    # train files init
    parse.parse_data('train', False)

    # Choose files you are needed
    # Full files
    pos_full_path = './created_files/pos_train.txt'
    sents_full_path = './created_files/sents_train.txt'

    # Experimental files (you can change it for yourself)
    pos_exp_path = './created_files/pos_exp.txt'
    sents_exp_path = './created_files/sents_exp.txt'

    # Initialize paths we work with
    pos_train_path = pos_exp_path
    sents_train_path = sents_exp_path
    init_train_data(pos_train_path, sents_train_path)

    # Write TRAIN_DATA for debug
    log = open('log.txt', 'w')
    log.write('\n'.join('%s' % str(el) for el in TRAIN_DATA))
    log.write('\n \n' + 'BATCHES:')

    nlp = spacy.load('en_core_web_sm')

    # TODO Find and fix crash for full-files
    #      Following code solved problem with hyphenated words
    def custom_tokenizer(nlp):
        infixes = (
                LIST_ELLIPSES
                + LIST_ICONS
                + [
                    r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                    r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                        al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                    ),
                    r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                    # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                    r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
                ]
        )

        infix_re = compile_infix_regex(infixes)

        return Tokenizer(nlp.vocab, prefix_search=nlp.tokenizer.prefix_search,
                         suffix_search=nlp.tokenizer.suffix_search,
                         infix_finditer=infix_re.finditer,
                         token_match=nlp.tokenizer.token_match,
                         rules=nlp.Defaults.tokenizer_exceptions)

    nlp = spacy.load('en_core_web_sm')
    nlp.tokenizer = custom_tokenizer(nlp)

    # #################################################################
    # ###################### SET UP MATCHER ###########################
    # #################################################################
    # It merges, but nlp.update does not see this or something like that

    matcher = Matcher(nlp.vocab)

    pattern = [{'ORTH': "'"},
               {'ORTH': 've'}]

    pattern_maj = [{'IS_ALPHA': "True"},
                   {'ORTH': '.'}]

    matcher.add('QUOTED', None, pattern, pattern_maj)

    def intra_hyphen_merger(doc):
        # this will be called on the Doc object in the pipeline
        matched_spans = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            matched_spans.append(span)
        for span in matched_spans:  # merge into one token after collecting all matches
            span.merge()
        return doc

    nlp.add_pipe(intra_hyphen_merger, first=True)  # add it right after the tokenizer

    optimizer = nlp.begin_training()
    for i in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))

        for batch in batches:
            texts, annotations = zip(*batch)

            # #########################################################################
            # ##########################  Log for debug  ##############################
            # #########################################################################
            log.write('\n\ni = ' + str(i+1))
            log.write('\nTEXTS:\n')
            log.write('\n'.join('%s' % str(text) for text in texts))
            log.write('\n\nANNOTATIONS:\n')
            log.write('\n'.join('%s' % str(ann) for ann in annotations))

            log.write('\n\nNLP SPLIT:\n')
            for sent in texts:
                nlp_split_sent = nlp(sent)
                log.write(''.join('%s ' % token.text for token in nlp_split_sent))
                log.write('\n')
            separator = "#" * 100
            log.write('\n' + separator)
            # ##########################################################################

            nlp.update(texts, annotations, sgd=optimizer, losses=losses)
            print("Losses", losses)
    log.close()

    # test the trained model
    test_text = "I like blue eggs"
    doc = nlp(test_text)
    print("Tags", [(t.text, t.tag_, t.pos_) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the save model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc = nlp2(test_text)
        print("Tags", [(t.text, t.tag_, t.pos_) for t in doc])


if __name__ == "__main__":
    plac.call(main)
