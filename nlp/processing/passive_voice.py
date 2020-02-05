import spacy
import text_processor as tp

#MODALS = ["must", "can", "should", "could", "may", "might"]
DEPENDENCIES = ["ROOT", "conj", "ccomp", "relcl", "acl", "advcl"]


def get_tense_rule(tense):
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
    nlp = spacy.load('en_core_web_sm')

    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)

    # make flexible batches (split at the end of the sentence)
    batch_indices = tp.flexible_batch_indices(text, 1000)
    text_split = [text[batch_indices[i-1]:batch_indices[i]] for i in range(1, len(batch_indices))]

    docs = list(nlp.pipe(text_split))

    tense_rule = get_tense_rule(tense)
    passive_phrases = []
    passive_phrases_lexemes = []
    passive_phrases_indices = []
    passive_phrases_sents = []

    for cur_batch, doc in enumerate(docs):
        for sent in doc.sents:
            for token in sent:
                if token.tag_ == 'VBN' and token.dep_ in DEPENDENCIES:
                    passive_match = []
                    passive_match_indices = []
                    passive_match_lexemes = []
                    num_of_aux = 0

                    prt_contained = False
                    subject_found = False

                    for child in token.children:
                        child_lower = child.text.lower()
                        if child.dep_ == 'nsubjpass':
                            passive_match.append(child.text)
                            if child.lemma_ == "-PRON-":
                                passive_match_lexemes.append(child.text)
                            else:
                                passive_match_lexemes.append(child.lemma_)
                            passive_match_indices.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])
                            subject_found = True

                        if child.dep_ == 'auxpass':
                            if child_lower in tense_rule.get('auxpass'):
                                passive_match.append(child.text)
                                passive_match_lexemes.append(child.lemma_)
                                passive_match_indices.append([child.idx - sent.start_char,
                                                              child.idx + len(child) - sent.start_char])
                            else:
                                passive_match = []
                                break

                        if child.dep_ == 'aux':
                            if child_lower in tense_rule.get('aux'):
                                num_of_aux += 1
                                passive_match.append(child.text)
                                passive_match_lexemes.append(child.lemma_)
                                passive_match_indices.append([child.idx - sent.start_char,
                                                              child.idx + len(child) - sent.start_char])
                            else:
                                passive_match = []
                                passive_match_lexemes = []
                                passive_match_indices = []
                                num_of_aux = 0
                                break

                        if child.dep_ == 'neg':
                            passive_match.append(child.text)
                            passive_match_lexemes.append(child.lemma_)
                            passive_match_indices.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])
                        if child.dep_ == 'prt':
                            passive_match.append(token.text)
                            passive_match.append(child.text)

                            passive_match_lexemes.append(token.lemma_)
                            passive_match_lexemes.append(child.lemma_)

                            passive_match_indices.append([token.idx - sent.start_char,
                                                          token.idx + len(token) - sent.start_char])
                            passive_match_indices.append([child.idx - sent.start_char,
                                                          child.idx + len(child) - sent.start_char])

                            prt_contained = True

                    if passive_match and subject_found and num_of_aux >= tense_rule.get('num_of_aux'):
                        if not prt_contained:
                            passive_match.append(token.text)
                            passive_match_lexemes.append(token.lemma_)
                            passive_match_indices.append([token.idx - sent.start_char,
                                                          token.idx + len(token) - sent.start_char])
                        batch_idx = batch_indices[cur_batch]
                        passive_phrases.append(passive_match)
                        passive_phrases_lexemes.append(passive_match_lexemes)
                        passive_phrases_indices.append(passive_match_indices)
                        passive_phrases_sents.append(text[batch_idx + sent.start_char:batch_idx + sent.end_char].strip())
                        pass

    result = [passive_phrases, passive_phrases_indices, passive_phrases_lexemes, passive_phrases_sents]
    return result
