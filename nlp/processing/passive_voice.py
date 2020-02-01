import spacy
import multiprocessing
import text_processor

from spacy.matcher import Matcher
from itertools import repeat

MODALS = ["must", "can", "should", "could", "may", "might"]
DEPENDENCIES = ["ROOT", "conj", "ccomp", "relcl", "acl", "advcl"]


def get_tense_rule(tense):
    tense_list = {
        "PRESENT_SIMPLE":
            dict(aux=[], auxpass=["am", "is", "are"]),
        "PRESENT_CONTINUOUS":
            dict(aux=["am", "is", "are"], auxpass=["being"]),
        "PRESENT_PERFECT":
            dict(aux=["have", "has"], auxpass=["been"]),

        "PAST_SIMPLE":
            dict(aux=[], auxpass=["was", "were"]),
        "PAST_CONTINUOUS":
            dict( aux=["was", "were"], auxpass=["being"]),
        "PAST_PERFECT":
            dict(aux=["had"], auxpass=["been"]),

        "FUTURE_SIMPLE":
            dict(aux=["shall", "will"], auxpass=["be"]),
        "FUTURE_PERFECT":
            dict(aux=["shall", "will", "have", "has"], auxpass=["been"]),
        "FUTURE_CONTINUOUS":
            dict(aux=["shall", "will", "be"], auxpass=["being"]),

        "FUTURE_IN_THE_PAST_SIMPLE":
            dict(aux=["would", "should"], auxpass=["be"]),
        "FUTURE_IN_THE_PAST_PERFECT":
            dict(aux=["would", "should", "have", "has"], auxpass=["been"]),

        "ALL":
            dict(aux=["am", "is", "are", "have", "has", "was", "were", "had", "shall", "will", "would", "should", "be"],
                 auxpass=["am", "is", "are", "was", "were", "being", "been", "be"])
    }
    return tense_list.get(tense, "all")


#############       Naive implementation     ###############
#############         Will be modified       ###############

def passive_voice_search(text, tense='all'):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)
    doc = nlp(text)

    tense_rule = get_tense_rule(tense)
    passive_phrases = []
    passive_phrases_lexemes = []
    passive_phrases_indexes = []
    passive_phrases_sents = []

    for sent in doc.sents:
        for token in sent:
            if token.tag_ == 'VBN' and token.dep_ in DEPENDENCIES:
                passive_match = []
                passive_match_indexes = []
                passive_match_lexemes = []

                prt_contained = False
                subject_found = False

                for child in token.children:
                    # print(child)
                    child_lower = child.text.lower()
                    if child.dep_ == 'nsubjpass':
                        passive_match.append(child.text)
                        if child.lemma_ == "-PRON-":
                            passive_match_lexemes.append(child.text)
                        else:
                            passive_match_lexemes.append(child.lemma_)
                        passive_match_indexes.append([child.idx - sent.start_char,
                                                      child.idx + len(child) - sent.start_char])
                        subject_found = True

                    if child.dep_ == 'auxpass':
                        if child_lower in tense_rule.get('auxpass'):
                            passive_match.append(child.text)
                            passive_match_lexemes.append(child.lemma_)
                            passive_match_indexes.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])

                        else:
                            passive_match = []
                            break

                    if child.dep_ == 'aux':
                        if child_lower in tense_rule.get('aux') or child_lower in MODALS:
                            passive_match.append(child.text)
                            passive_match_lexemes.append(child.lemma_)
                            passive_match_indexes.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])
                        else:
                            passive_match = []
                            passive_match_lexemes = []
                            passive_match_indexes = []
                            break

                    if child.dep_ == 'neg':
                        passive_match.append(child.text)
                        passive_match_lexemes.append(child.lemma_)
                        passive_match_indexes.append([child.idx - sent.start_char,
                                                      child.idx + len(child) - sent.start_char])

                    if child.dep_ == 'prt':
                        passive_match.append(token.text)
                        passive_match.append(child.text)

                        passive_match_lexemes.append(token.lemma_)
                        passive_match_lexemes.append(child.lemma_)

                        passive_match_indexes.append([token.idx - sent.start_char,
                                                      token.idx + len(token) - sent.start_char])
                        passive_match_indexes.append([child.idx - sent.start_char,
                                                      child.idx + len(child) - sent.start_char])

                        prt_contained = True

                if passive_match and subject_found:
                    if not prt_contained:
                        passive_match.append(token.text)
                        passive_match_lexemes.append(token.lemma_)
                        passive_match_indexes.append([token.idx - sent.start_char,
                                                      token.idx + len(token) - sent.start_char])

                    passive_phrases.append(passive_match)
                    passive_phrases_lexemes.append(passive_match_lexemes)
                    passive_phrases_indexes.append(passive_match_indexes)
                    passive_phrases_sents.append(text[sent.start_char:sent.end_char].strip())
                    pass
    result = [passive_phrases, passive_phrases_indexes, passive_phrases_lexemes, passive_phrases_sents]

    # print("\nSimple")
    # for ppidx in passive_phrases_indexes:
    #     print(str(ppidx) + " ")
    # for el in result:
    #     print(el)
    #     print("\n")
    return result


def passive_voice_search_batches(text, tense='all'):
    nlp = spacy.load('en_core_web_sm')
    #nlp.max_length = 1500000

    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)

    # make flexible batches (split at the end of the sentence)
    batch_indices = text_processor.flexible_batch_indices(text, 1000)
    text_split = [text[batch_indices[i-1]:batch_indices[i]] for i in range(1, len(batch_indices))]

    docs = list(nlp.pipe(text_split))

    tense_rule = get_tense_rule(tense)
    passive_phrases = []
    passive_phrases_lexemes = []
    passive_phrases_indexes = []
    passive_phrases_sents = []
    cur_batch = 0

    for doc in docs:
        for sent in doc.sents:
            for token in sent:
                if token.tag_ == 'VBN' and token.dep_ in DEPENDENCIES:
                    passive_match = []
                    passive_match_indexes = []
                    passive_match_lexemes = []

                    prt_contained = False
                    subject_found = False

                    for child in token.children:
                        #print(child)
                        child_lower = child.text.lower()
                        if child.dep_ == 'nsubjpass':
                            passive_match.append(child.text)
                            if child.lemma_ == "-PRON-":
                                passive_match_lexemes.append(child.text)
                            else:
                                passive_match_lexemes.append(child.lemma_)
                            passive_match_indexes.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])
                            subject_found = True

                        if child.dep_ == 'auxpass':
                            if child_lower in tense_rule.get('auxpass'):
                                passive_match.append(child.text)
                                passive_match_lexemes.append(child.lemma_)
                                passive_match_indexes.append([child.idx - sent.start_char,
                                                              child.idx + len(child) - sent.start_char])

                            else:
                                passive_match = []
                                break

                        if child.dep_ == 'aux':
                            if child_lower in tense_rule.get('aux') or child_lower in MODALS:
                                passive_match.append(child.text)
                                passive_match_lexemes.append(child.lemma_)
                                passive_match_indexes.append([child.idx - sent.start_char,
                                                              child.idx + len(child) - sent.start_char])
                            else:
                                passive_match = []
                                passive_match_lexemes = []
                                passive_match_indexes = []
                                break

                        if child.dep_ == 'neg':
                            passive_match.append(child.text)
                            passive_match_lexemes.append(child.lemma_)
                            passive_match_indexes.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])

                        if child.dep_ == 'prt':
                            passive_match.append(token.text)
                            passive_match.append(child.text)

                            passive_match_lexemes.append(token.lemma_)
                            passive_match_lexemes.append(child.lemma_)

                            passive_match_indexes.append([token.idx - sent.start_char,
                                                          token.idx + len(token) - sent.start_char])
                            passive_match_indexes.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])

                            prt_contained = True

                    if passive_match and subject_found:
                        if not prt_contained:
                            passive_match.append(token.text)
                            passive_match_lexemes.append(token.lemma_)
                            passive_match_indexes.append([token.idx - sent.start_char,
                                                          token.idx + len(token) - sent.start_char])

                        batch_idx = batch_indices[cur_batch]
                        passive_phrases.append(passive_match)
                        passive_phrases_lexemes.append(passive_match_lexemes)
                        passive_phrases_indexes.append(passive_match_indexes)
                        passive_phrases_sents.append(text[batch_idx + sent.start_char:batch_idx + sent.end_char].strip())
                        pass
        cur_batch += 1

    result = [passive_phrases, passive_phrases_indexes, passive_phrases_lexemes, passive_phrases_sents]
    return result


def passive_voice_search_exp(text, tense='all'):
    nlp = spacy.load('en_core_web_sm')

    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)

    # TODO: make flexible batches (split at the end of the sentence)
    n = 1000
    text_splited = [text[i:i + n] for i in range(0, len(text), n)]
    docs = list(nlp.pipe(text_splited))

    tense_rule = get_tense_rule(tense)
    passive_phrases = []
    for doc in docs:
        i = 0
        while i < len(doc):
            token = doc[i]
            if token.dep_ == 'nsubjpass':
                passive_match = []
                prt_contained = False
                head_token = token.head

                for child in head_token.children:
                    # print(child)
                    child_lower = child.text.lower()
                    if child.dep_ == 'nsubjpass':
                        passive_match.append(child.text)
                        # subject_found = True

                    if child.dep_ == 'auxpass':
                        if child_lower in tense_rule.get('auxpass'):
                            passive_match.append(child.text)
                        else:
                            passive_match = []
                            break

                    if child.dep_ == 'aux':
                        if child_lower in tense_rule.get('aux') or child_lower in MODALS:
                            passive_match.append(child.text)
                        else:
                            passive_match = []
                            break

                    if child.dep_ == 'neg':
                        passive_match.append(child.text)

                    if child.dep_ == 'prt':
                        passive_match.append(head_token.text)
                        passive_match.append(child.text)
                        prt_contained = True

                if not prt_contained:
                    passive_match.append(head_token.text)
                passive_phrases.append(' '.join(passive_match))

                i = token.head.i + 1
            else:
                i += 1

    return passive_phrases


# def passive_voice_search_multiprocessing(text, tense):
#     nlp = spacy.load('en_core_web_sm')
#     nlp.max_length = 1500000
#
#     merge_ents = nlp.create_pipe("merge_entities")
#     merge_nps = nlp.create_pipe("merge_noun_chunks")
#     nlp.add_pipe(merge_nps, merge_ents)
#     doc = nlp(text)
#
#     tense_rule = get_tense_rule(tense)
#
#     with multiprocessing.Pool() as pool:
#         passive_phrases = pool.starmap(dependency_tree_analysis,  zip(doc.sents, repeat(tense_rule)))
#
#     return passive_phrases


def matcher_passive_voice_search(text):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    matcher = Matcher(nlp.vocab)
    # doc = nlp(text)

    n = 1000
    text_splited = [text[i:i + n] for i in range(0, len(text), n)]
    docs = list(nlp.pipe(text_splited))

    passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
    matcher.add('Passive', None, passive_rule)

    passive_phrases = []
    for doc in docs:
        matches = matcher(doc)
        for match in matches:
            passive_phrases.append(doc[match[1]:match[2]].text)
    return passive_phrases
