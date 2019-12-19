from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.tokenizer import Tokenizer
import os

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
    mail = os.linesep.join([s for s in mail.splitlines() if s])
    mail = replace_canadian_period(mail)
    mail = replace_fancy_hyphens(mail)
    return mail


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