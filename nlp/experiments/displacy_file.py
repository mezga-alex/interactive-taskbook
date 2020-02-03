import spacy
from spacy import displacy
import text_processor as tp
from spacy.matcher import Matcher


def displacy_func(text):
    nlp = spacy.load('en_core_web_sm')

    nlp.tokenizer = tp.custom_tokenizer(nlp)
    # nlp = tp.custom_matcher(nlp)

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

    # batch_indices = tp.flexible_batch_indices(text, 1000)
    # text_split = [text[batch_indices[i - 1]:batch_indices[i]] for i in range(1, len(batch_indices))]
    #
    # docs = list(nlp.pipe(text_split))

    doc = nlp(text[0:500])
    html = displacy.render(doc, style="ent", page=True)

    Html_file = open("displacy.html", "w")
    Html_file.write(html)
    Html_file.close()
