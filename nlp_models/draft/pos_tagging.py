import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.matcher import Matcher

import parse


# Change different dashes to the standard
def replace_canadian_period(mail):
    mail = mail.replace(u"\u1427", ".")
    return mail


def replace_fancy_hyphens(mail):
    hlist = [u"\u002d", u"\u058a", u"\u058b", u"\u2010", u"\u2011", u"\u2012", u"\u2013",
             u"\u2014", u"\u2015", u"\u2e3a", u"\u2e3b", u"\ufe58", u"\ufe63", u"\uff0d"]
    for h in hlist:
        mail = mail.replace(h, "-")
    return mail


def lexical_processor(mail):
    mail = replace_canadian_period(mail)
    mail = replace_fancy_hyphens(mail)
    return mail


parse.parse_data('test')
text = lexical_processor(open('./created_files/text_test.txt').read())
pos = open('./created_files/pos_test.txt').read()


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

# #################################################################
# ###################### SET UP MATCHER ###########################
# #################################################################

matcher = Matcher(nlp.vocab)

pattern = [{'ORTH': "'"},
           {'ORTH': 've'}]

pattern_2 = [{'ORTH': "'"},
           {'ORTH': 'm'}]

# pattern_3 = [{'LIKE_NUM': "True"},
#              {'ORTH': '-'},
#              {'LIKE_NUM': "True"}]

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

nlp_res = []
for token in doc:
    nlp_res.append([token.text, token.tag_])

text = text.split()
pos = pos.split()
parse_res = []
for word, pos_tag in zip(text, pos):
    parse_res.append([word, pos_tag])


#print(abs(len(nlp_res) - len(parse_res)))

# For debug (create file with different lines) + ACCURACY component
file_compare = open('./created_files/compare_res.txt', 'w')
correct_predict = 0
for nlp_line, parse_line in zip(nlp_res, parse_res):
    if nlp_line[0] == parse_line[0]:
        if nlp_line[1] == parse_line[1]:
            correct_predict += 1
    else:
        file_compare.write(str(nlp_line) + '     ' + str(parse_line) + '\n')

file_compare.close()

accuracy = correct_predict / len(parse_res) * 100

print('Words found ' + str(len(nlp_res)))
print('Test set size (words): ' + str(len(parse_res)))
print('Accuracy (POS-tagging): ' + str(accuracy) + '%')
