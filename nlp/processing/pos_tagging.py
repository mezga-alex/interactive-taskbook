import spacy
import text_processor
from spacy.matcher import Matcher


def pos_tag_search(pos_tag, text):
    nlp = spacy.load('en_core_web_sm')
    nlp.tokenizer = text_processor.custom_tokenizer(nlp)
    nlp.max_length = 1500000

    # #################################################################
    # ###################### SET UP MATCHER ###########################
    # #################################################################

    matcher = Matcher(nlp.vocab)

    pattern = [{'ORTH': "'"},
               {'ORTH': 've'}]

    pattern_2 = [{'ORTH': "'"},
                 {'ORTH': 'm'}]

    matcher.add('QUOTED', None, pattern, pattern_2)

    def match_merger(doc):
        # this will be called on the Doc object in the pipeline
        matched_spans = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            matched_spans.append(span)
        for span in matched_spans:  # merge into one token after collecting all matches
            span.merge()
        return doc

    nlp.add_pipe(match_merger, first=True)  # add it right after the tokenizer
    # #################################################################

    doc = nlp(text)

    tokens = []
    index = 0
    for token in doc:
        if token.pos_ == pos_tag:
            tokens.append([token.text, index])

    return tokens
