import spacy
import multiprocessing

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

def passive_voice_search(text, tense = 'all'):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)
    doc = nlp(text)

    tense_rule = get_tense_rule(tense)
    passive_phrases = []
    for sent in doc.sents:
        for token in sent:
            if token.tag_ == 'VBN' and token.dep_ in DEPENDENCIES:
                passive_match = []
                prt_contained = False
                subject_found = False

                for child in token.children:
                    #print(child)
                    child_lower = child.text.lower()
                    if child.dep_ == 'nsubjpass':
                        passive_match.append(child.text)
                        subject_found = True

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
                        passive_match.append(token.text)
                        passive_match.append(child.text)
                        prt_contained = True

                if passive_match and subject_found:
                    if not prt_contained:
                        passive_match.append(token.text)
                    passive_phrases.append(' '.join(passive_match))

    return passive_phrases


def dependency_tree_analysis(sent, tense_rule):
    for token in sent:
        if token.tag_ == 'VBN' and token.dep_ in DEPENDENCIES:
            passive_match = []
            prt_contained = False
            subject_found = False

            for child in token.children:
                # print(child)
                child_lower = child.text.lower()
                if child.dep_ == 'nsubjpass':
                    passive_match.append(child.text)
                    subject_found = True

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
                    passive_match.append(token.text)
                    passive_match.append(child.text)
                    prt_contained = True

            if passive_match and subject_found:
                if not prt_contained:
                    passive_match.append(token.text)

                return ' '.join(passive_match)


def passive_voice_search_multiprocessing(text, tense):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)
    doc = nlp(text)

    tense_rule = get_tense_rule(tense)

    with multiprocessing.Pool() as pool:
        passive_phrases = pool.starmap(dependency_tree_analysis,  zip(doc.sents, repeat(tense_rule)))

    return passive_phrases


def matcher_passive_voice_search(text):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    matcher = Matcher(nlp.vocab)
    doc = nlp(text)

    passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
    matcher.add('Passive', None, passive_rule)
    matches = matcher(doc)
    passive_phrases = []

    for match in matches:
        passive_phrases.append(doc[match[1]:match[2]].text)
    return passive_phrases
