import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

# nlp = spacy.load('en_core_web_sm')
#
# matcher = Matcher(nlp.vocab)
#
# pattern_have = [{'ORTH': "'"},
#                 {'ORTH': 've'}]
# pattern = [{'IS_ASCII': True, 'OP': '?'},
#            {'ORTH': '-'},
#            {'IS_ALPHA': True}]
#
# matcher.add('QUOTED', None, pattern, pattern_have)
#

# def intra_hyphen_merger(doc):
#     # this will be called on the Doc object in the pipeline
#     matched_spans = []
#     matches = matcher(doc)
#
#     for match_id, start, end in matches:
#         span = doc[start:end]
#         matched_spans.append(span)
#
#     def filter_spans(spans, prefer_longest=True):
#         # Filter a sequence of spans so they don't contain overlaps
#         get_sort_key = lambda span: (span.end - span.start, span.start)
#         sorted_spans = sorted(spans, key=get_sort_key, reverse=prefer_longest)
#         result = []
#         seen_tokens = set()
#         for span in spans:
#             if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
#                 result.append(span)
#                 seen_tokens.update(range(span.start, span.end))
#         return result
#
#
#     print(str(matched_spans))
#     matched_spans = filter_spans(matched_spans)
#     print(str(matched_spans))
#
#     with doc.retokenize() as retokenizer:
#         i = 0
#         for span in matched_spans:
#             # print(span)
#             # print(str(span[0]))
#             # print('----------')
#             if str(span[0]) == '-':
#                 matched_spans[i - 1] =
#             i += 1
#             retokenizer.merge(span)
#
#     for span in matched_spans:  # merge into one token after collecting all matches
#         span.merge()
#     return doc

# nlp.add_pipe(intra_hyphen_merger, first=True)  # add it right after the tokenizer


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
            #r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
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

doc = nlp("We it's have been you've la-la qwerty q-w-e a-s-d-f-g-h-123")
print([token.text for token in doc])
