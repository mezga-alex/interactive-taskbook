from spacy.matcher import Matcher
import spacy
import text_processor as tp

MODALS = ["must", "can", "should", "could", "may", "might"]
#DEPENDENCIES = ["ROOT", "advcl", "acl", "xcomp", "ccomp", "conj", "relcl"]


def get_active_tense_rule(tense):
    tense_list = {
        "PRESENT_SIMPLE":
            dict(aux=["do", "does"], vtag=["VBP", "VBZ"]),
        "PRESENT_CONTINUOUS":
            dict(aux=["am", "is", "are"], vtag=["VBG"]),
        "PRESENT_PERFECT":
            dict(aux=["have", "has"], vtag=["VBN"]),

        "PAST_SIMPLE":
            dict(aux=["did"], vtag=["VBD"]),
        "PAST_CONTINUOUS":
            dict(aux=["was", "were"], vtag=["VBG"]),
        "PAST_PERFECT":
            dict(aux=["had"], vtag=["VBN"]),

        "FUTURE_SIMPLE":
            dict(aux=["shall", "will"], vtag=["VB"]),
        "FUTURE_PERFECT":
            dict(aux=["shall", "will", "have", "has"], vtag=["VBN"]),
        "FUTURE_CONTINUOUS":
            dict(aux=["shall", "will", "be"], vtag=["VBG"]),
        "ALL":
            dict(aux=["do", "does", "did", "am", "is", "are", "have", "has", "was", "were", "had", "shall", "will",
                      "would", "should", "be"],
                 vtag=["VB", "VBZ", "VBP", "VBG", "VBN", "VBD"])
    }
    return tense_list.get(tense, "ALL")


def active_voice_search_batches(text, tense='ALL'):
    nlp = spacy.load('en_core_web_sm')


    merge_ents = nlp.create_pipe("merge_entities")
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps, merge_ents)

    text = tp.lexical_processor(text)

    batch_indices = tp.flexible_batch_indices(text, 1000)
    text_split = [text[batch_indices[i - 1]:batch_indices[i]] for i in range(1, len(batch_indices))]

    docs = list(nlp.pipe(text_split))

    tense_rule = get_active_tense_rule(tense)

    active_phrases = []
    active_phrases_lexemes = []
    active_phrases_indices = []
    active_phrases_sents = []

    for cur_batch, doc in enumerate(docs):
        for sent in doc.sents:
            for token in sent:
                if token.tag_ in tense_rule.get('vtag'):
                    active_match = []
                    active_match_indices = []
                    active_match_lexemes = []

                    to_inf_match = []
                    subject_found = False
                    prt_contained = False

                    for child in token.children:
                        child_lower = child.text.lower()
                        if child.dep_ == 'nsubj':
                            active_match.append(child.text)
                            if child.lemma_ == "-PRON-":
                                active_match_lexemes.append(child.text)
                            else:
                                active_match_lexemes.append(child.lemma_)
                            active_match_indices.append([child.idx - sent.start_char,
                                                         child.idx + len(child) - sent.start_char])
                            subject_found = True

                        if child.dep_ == 'auxpass':
                            active_match = []
                            active_match_indices =[]
                            active_match_lexemes =[]
                            break
                        if child.dep_ == 'aux':
                            if child_lower in tense_rule.get('aux') or child_lower in MODALS:
                                active_match.append(child.text)
                                active_match_lexemes.append(child.lemma_)
                                active_match_indices.append([child.idx - sent.start_char,
                                                             child.idx + len(child) - sent.start_char])
                            else:
                                active_match = []
                                active_match_lexemes = []
                                active_match_indices = []
                                break

                        if child.dep_ == 'xcomp':
                            for grandchild in child.children:
                                if grandchild.dep_ == 'aux':
                                    to_inf_match.append(grandchild)

                            to_inf_match.append(child)

                        if child.dep_ == 'neg':
                            active_match.append(child.text)
                            active_match_lexemes.append(child.lemma_)
                            active_match_indices.append([child.idx - sent.start_char,
                                                         child.idx + len(child) - sent.start_char])
                        if child.dep_ == 'prt':
                            active_match.append(token.text)
                            active_match.append(child.text)

                            active_match_lexemes.append(token.lemma_)
                            active_match_lexemes.append(child.lemma_)

                            active_match_indices.append([token.idx - sent.start_char,
                                                         token.idx + len(token) - sent.start_char])
                            active_match_indices.append([child.idx - sent.start_char,
                                                         child.idx + len(child) - sent.start_char])

                            prt_contained = True
                    if active_match and subject_found:
                        if not prt_contained:
                            active_match.append(token.text)
                            active_match_lexemes.append(token.lemma_)
                            active_match_indices.append([token.idx - sent.start_char,
                                                         token.idx + len(token) - sent.start_char])
                        if to_inf_match:
                            [active_match.append(t.text) for t in to_inf_match]
                            [active_match_lexemes.append(t.lemma_) for t in to_inf_match]
                            [active_match_indices.append([t.idx - sent.start_char,
                                                         t.idx + len(t) - sent.start_char]) for t in to_inf_match]
                        batch_idx = batch_indices[cur_batch]
                        active_phrases.append(active_match)
                        active_phrases_lexemes.append(active_match_lexemes)
                        active_phrases_indices.append(active_match_indices)
                        active_phrases_sents.append(text[batch_idx + sent.start_char:batch_idx + sent.end_char].strip())
                        pass
        result = [active_phrases, active_phrases_indices, active_phrases_lexemes, active_phrases_sents]
        return result
