"""Text processing before use.

We make some manipulations before submitting text to the input of the NLP model.
- Replace some non-standard symbols.
- Change standard tokenizer.
- Change standard matcher.
"""

from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.tokenizer import Tokenizer
from spacy.matcher import Matcher

import os
import re


def replace_canadian_period(text):
    text = text.replace(u"\u1427", ".")
    return text


def replace_fancy_hyphens(text):
    hlist = [u"\u002d", u"\u058a", u"\u058b", u"\u2010", u"\u2011", u"\u2012", u"\u2013",
             u"\u2014", u"\u2015", u"\u2e3a", u"\u2e3b", u"\ufe58", u"\ufe63", u"\uff0d"]
    for h in hlist:
        text = text.replace(h, "-")
    return text


def lexical_processor(text):
    """Gets raw text and returns processed.

    Parameters
    ----------
    text : str
        Text for analysis.

    Returns
    -------
    text : str
        Processed text for the NLP Model.
    """
    text = os.linesep.join([s for s in text.splitlines() if s])
    text = replace_canadian_period(text)
    text = replace_fancy_hyphens(text)
    return text


def custom_tokenizer(nlp):
    """Change tokenizer of the NLP Model.

    Parameters
    ----------
    nlp :
        Loaded NLP Model.

    Returns
    -------
    Tokenizer(nlp)
        NLP Model with custom tokenizer.
    """

    # Exclude dashes from infixes
    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
        ]
    )

    infix_re = compile_infix_regex(infixes)

    return Tokenizer(nlp.vocab, prefix_search=nlp.tokenizer.prefix_search,
                                suffix_search=nlp.tokenizer.suffix_search,
                                infix_finditer=infix_re.finditer,
                                token_match=nlp.tokenizer.token_match,
                                rules=nlp.Defaults.tokenizer_exceptions)


# TODO: Fix incorrect return
def custom_matcher(nlp):
    """Change matcher of the NLP Model.

    Parameters
    ----------
    nlp :
        Loaded NLP Model.

    Returns
    -------
    Tokenizer(nlp)
        NLP Model with custom matcher.
    """

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

    return nlp.add_pipe(match_merger, first=True)


# TODO: Fix problems with several abbreviation (eg. "Dr. Who")
def flexible_batch_indices(text, approximate_batch_size):
    """Find the borders of the batches.

    Using batches is much more efficient than raw text..

    Parameters
    ----------
    text : str
        Text for analysis.

    approximate_batch_size: int
        Estimated batches size in characters.

    Returns
    -------
    batch_indices: list
       List of indices of the end of batches.
    """

    exp = r'[.?!](?= [A-Z]|$)'
    cur_index = 0
    find_start = 0
    batch_indices = [0]
    sentence_found = False

    # Continue while start index < text length.
    while find_start < len(text):
        find_start = cur_index + approximate_batch_size
        find_end = find_start + approximate_batch_size

        # Check if the right index is less or equal to the length of the text.
        if find_end > len(text):
            find_end = len(text)

        # Use Regex to find the end of a sentence in a text span.
        match = re.search(exp, text[find_start:find_end])
        # If a match is found, recalculate the indices and add to the list.
        if match:
            cur_index = match.end() + find_start - 1
            batch_indices.append(cur_index)
            sentence_found = True
        else:
            # Just shift the index otherwise.
            cur_index += approximate_batch_size
            sentence_found = False

    # Add the last index if there is significant text at the end of the raw text.
    if sentence_found:
        batch_indices.append(len(text))

    return batch_indices
