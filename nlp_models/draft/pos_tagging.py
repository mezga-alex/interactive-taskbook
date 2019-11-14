# IF THERE IS NO ANY FILE, RUN PARSE.PY FIRST
import spacy
from spacy.tokenizer import Tokenizer


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


# Read from files
# Text.txt and Pos.txt were parsed from the test dataset
text = lexical_processor(open('text.txt').read())
pos = open('pos.txt').read()

nlp = spacy.load('en_core_web_sm')
# TODO: decide and implement the correct version of tokenization
infixes = nlp.Defaults.prefixes + (r"[./]", r"[-]~", r"(.'.)")
infix_re = spacy.util.compile_infix_regex(infixes)


def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, infix_finditer=infix_re.finditer)


nlp.tokenizer = custom_tokenizer(nlp)

doc = nlp(text)
# Create Tuple (WORD, POS_TAG) with the model.
nlp_res = [(token.text, token.tag_) for token in doc]
print(nlp_res)

print()
text = text.split()
pos = pos.split()

# Create Tuple (WORD, POS_TAG) with the parsed data.
pars_res = [(text[i], pos[i]) for i in range(len(pos))]
print(pars_res)

# TODO: fully understand the following situation
print('WTF?: nlp_length', len(nlp_res),' parsed_length', len(pars_res))

# Write down results of POS-Tagging work
# Parsed data is available in test.txt (dataset) for comparison with result
with open('results_nlp.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in pars_res))
