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
text = lexical_processor(open('./created_files/text.txt').read())
pos = open('./created_files/pos.txt').read()

nlp = spacy.load('en_core_web_sm')
# TODO: decide and implement the correct version of tokenization
infixes = nlp.Defaults.prefixes + tuple(r"[-]~")
infix_re = spacy.util.compile_infix_regex(infixes)


def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, infix_finditer=infix_re.finditer)


nlp.tokenizer = custom_tokenizer(nlp)

doc = nlp(text)

# Create Tuple (WORD, POS_TAG) with the model.
nlp_res = []
for token in doc:
    if not token.is_punct and token.tag_ != '$':
        nlp_res.append((token.text, token.tag_))
#print(nlp_res)

#print()
text = text.split()
pos = pos.split()

# Create Tuple (WORD, POS_TAG) with the parsed data.
pars_res = []
for i in range(len(pos)):
    if len(pos[i]) > 1:
        pars_res.append((text[i], pos[i]))
#print(pars_res)

# TODO: fully understand the following situation
# We ignored empty lines and lines with only non-alphabetical symbols
print('WTF?: nlp_length', len(nlp_res),' parsed_length', len(pars_res))

# Write down results of POS-Tagging work
# Parsed data is available in test.txt (dataset) for comparison with result
with open('./created_files/results_nlp.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in nlp_res))

with open('./created_files/results_parse.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in pars_res))
