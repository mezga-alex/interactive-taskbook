"""Passive Voice Search.

Passive voice search algorithm in the text.
- Prepare raw text.
- Use the NLP model.
- Use rule-based algorithm.
- Return results.
"""

import spacy
import text_processor as tp

# Possible dependencies between words.
DEPENDENCIES = ["ROOT", "conj", "ccomp", "relcl", "acl", "advcl"]


def get_tense_rule(tense):
    """Function to take the rules for a certain tense."""

    tense_list = {
        "PRESENT_SIMPLE":
            dict(aux=[], auxpass=["am", "is", "are"], num_of_aux=0),
        "PRESENT_CONTINUOUS":
            dict(aux=["am", "is", "are"], auxpass=["being"], num_of_aux=1),
        "PRESENT_PERFECT":
            dict(aux=["have", "has"], auxpass=["been"], num_of_aux=1),

        "PAST_SIMPLE":
            dict(aux=[], auxpass=["was", "were"], num_of_aux=0),
        "PAST_CONTINUOUS":
            dict( aux=["was", "were"], auxpass=["being"], num_of_aux=1),
        "PAST_PERFECT":
            dict(aux=["had"], auxpass=["been"], num_of_aux=1),

        "FUTURE_SIMPLE":
            dict(aux=["shall", "will"], auxpass=["be"], num_of_aux=1),
        "FUTURE_PERFECT":
            dict(aux=["shall", "will", "have", "has"], auxpass=["been"], num_of_aux=2),
        "FUTURE_CONTINUOUS":
            dict(aux=["shall", "will", "be"], auxpass=["being"], num_of_aux=2),

        "FUTURE_IN_THE_PAST_SIMPLE":
            dict(aux=["would", "should"], auxpass=["be"], num_of_aux=1),
        "FUTURE_IN_THE_PAST_PERFECT":
            dict(aux=["should", "would", "have", "has"], auxpass=["been"], num_of_aux=2),

        "MODALS":
            dict(aux=["must", "can", "should", "could", "would", "may", "might", "have"],
                 auxpass=["be", "been"], num_of_aux=1),

        "ALL":
            dict(aux=["am", "is", "are", "have", "has", "was", "were", "had", "shall", "will", "would", "should", "be",
                      "must", "can", "could", "may", "might"],
                 auxpass=["am", "is", "are", "was", "were", "being", "been", "be"], num_of_aux=0)
    }

    return tense_list.get(tense, "ALL")


def passive_voice_search_batches(text, tense='ALL'):
    """Search for passive voices for a given tense.

    Using batches is much more efficient than raw text..

    Parameters
    ----------
    text : str
        Text for analysis.

    tense: str
        Given tense for search.

    Returns
    -------
    result: list
       List contains:
       1. Passive verbs.
       2. Indexes of found phrases.
       3. Initial forms of words.
       4. Sentences that contain phrases.
    """

    nlp = spacy.load('en_core_web_sm')

    # NLP model preparation
    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)

    # Text preparation
    text = tp.lexical_processor(text)

    # Create flexible batches (split at the end of the sentence)
    batch_indices = tp.flexible_batch_indices(text, 1000)
    text_split = [text[batch_indices[i-1]:batch_indices[i]] for i in range(1, len(batch_indices))]

    # Apply the model to batches
    docs = list(nlp.pipe(text_split))
    # Take the rules for the right tense
    tense_rule = get_tense_rule(tense)

    # Lists needed to return a result
    passive_phrases = []
    passive_phrases_lexemes = []
    passive_phrases_indices = []
    passive_phrases_sents = []

    # Start navigating the dependency tree
    for cur_batch, doc in enumerate(docs):
        for sent in doc.sents:
            for token in sent:
                # Define the main word
                if token.tag_ == 'VBN' and token.dep_ in DEPENDENCIES:
                    passive_match = []
                    passive_match_indices = []
                    passive_match_lexemes = []
                    num_of_aux = 0
                    num_of_aux_rule = tense_rule.get('num_of_aux')  #It is necessary for correct work with modals.

                    prt_contained = False
                    subject_found = False

                    # Navigate on its children
                    for child in token.children:
                        child_lower = child.text.lower()
                        # We consider several options for the dependencies of these words:
                        # 1: A passive nominal subject
                        # 2: A passive auxiliary of a clause
                        # 3: An auxiliary of a clause
                        # 4: The negation modifier
                        # 5: The phrasal verb particle
                        # Add parameters for the found match.

                        # 1: A passive nominal subject
                        if child.dep_ == 'nsubjpass':
                            passive_match.append(child.text)
                            if child.lemma_ == "-PRON-":
                                passive_match_lexemes.append(child.text)
                            else:
                                passive_match_lexemes.append(child.lemma_)
                            passive_match_indices.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])
                            subject_found = True

                        # 2: A passive auxiliary of a clause
                        if child.dep_ == 'auxpass':
                            if child_lower in tense_rule.get('auxpass'):
                                passive_match.append(child.text)
                                passive_match_lexemes.append(child.lemma_)
                                passive_match_indices.append([child.idx - sent.start_char,
                                                              child.idx + len(child) - sent.start_char])
                            else:
                                # If we find a match but from another tense => skip
                                passive_match = []
                                passive_match_lexemes = []
                                passive_match_indices = []
                                num_of_aux = 0
                                num_of_aux_rule = tense_rule.get('num_of_aux')
                                break

                        # 3: An auxiliary of a clause
                        if child.dep_ == 'aux':
                            if child_lower in tense_rule.get('aux'):
                                num_of_aux += 1
                                passive_match.append(child.text)
                                passive_match_lexemes.append(child.lemma_)
                                passive_match_indices.append([child.idx - sent.start_char,
                                                              child.idx + len(child) - sent.start_char])

                                # If Modals with Passive in past tense the number of aux is more than 2
                                if tense == 'MODALS' and child_lower == 'have':
                                    num_of_aux_rule += 1
                            else:
                                # If we find a match but from another tense => skip
                                passive_match = []
                                passive_match_lexemes = []
                                passive_match_indices = []
                                num_of_aux = 0
                                num_of_aux_rule = tense_rule.get('num_of_aux')
                                break

                        # 4: The negation modifier
                        if child.dep_ == 'neg':
                            passive_match.append(child.text)
                            passive_match_lexemes.append(child.lemma_)
                            passive_match_indices.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])

                        # 5: The phrasal verb particle
                        if child.dep_ == 'prt':
                            # If The phrasal verb particle is contained, save not only the child but also the token
                            passive_match.append(token.text)
                            passive_match.append(child.text)

                            passive_match_lexemes.append(token.lemma_)
                            passive_match_lexemes.append(child.lemma_)

                            passive_match_indices.append([token.idx - sent.start_char,
                                                          token.idx + len(token) - sent.start_char])
                            passive_match_indices.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])
                            # Flag for proper word placement
                            prt_contained = True

                    # Check if a relevant phrase was found in which the subject was found
                    # with an additional check to avoid conflicts
                    if passive_match and subject_found and num_of_aux >= num_of_aux_rule:
                        # If The phrasal verb particle is contained, the word order is changed and taken into account
                        if not prt_contained:
                            passive_match.append(token.text)
                            passive_match_lexemes.append(token.lemma_)
                            passive_match_indices.append([token.idx - sent.start_char,
                                                          token.idx + len(token) - sent.start_char])

                        # Use batch_idx to correctly determine the index in the raw text
                        batch_idx = batch_indices[cur_batch]
                        passive_phrases.append(passive_match)
                        passive_phrases_lexemes.append(passive_match_lexemes)
                        passive_phrases_indices.append(passive_match_indices)
                        passive_phrases_sents.append(text[batch_idx + sent.start_char:batch_idx + sent.end_char].strip())
                        pass

    # Return the found phrases, their indices, word lexemes, their sentences
    result = [passive_phrases, passive_phrases_indices, passive_phrases_lexemes, passive_phrases_sents]
    return result
