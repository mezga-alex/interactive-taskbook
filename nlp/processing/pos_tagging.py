import spacy
import text_processor as tp
from spacy.matcher import Matcher


def pos_tag_search(text, pos_tag):
    nlp = spacy.load('en_core_web_sm')

    nlp.tokenizer = tp.custom_tokenizer(nlp)
    #nlp = tp.custom_matcher(nlp)

    # ############## Custom Matcher #########################

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

    nlp.add_pipe(match_merger, first=True)
    # ########################################################

    batch_indices = tp.flexible_batch_indices(text, 1000)
    text_split = [text[batch_indices[i-1]:batch_indices[i]] for i in range(1, len(batch_indices))]

    docs = list(nlp.pipe(text_split))

    tokens = []
    tokens_indices = []
    tokens_pos = []
    include_all_pos = pos_tag == 'ALL'
    for cur_batch, doc in enumerate(docs):
        batch_idx = batch_indices[cur_batch]
        for token in doc:
            if (token.pos_ == pos_tag or include_all_pos) and token.pos_ != 'PUNCT':
                tokens.append(token.text)
                tokens_indices.append([batch_idx + token.idx,
                                       batch_idx + token.idx + len(token)])
                if include_all_pos:
                    tokens_pos.append(token.pos_)

    result = [tokens, tokens_indices]
    if include_all_pos:
        result.append(tokens_pos)

    return result

