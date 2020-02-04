###########################
#  Draft for experiments  #
###########################

import spacy
from spacy import displacy
from spacy.matcher import Matcher

import time

from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.matcher import Matcher

#
# def set_custom_boundaries(doc):
#     # Adds support to use `...` as the delimiter for sentence detection
#     for token in doc[:-1]:
#         if token.text == '...':
#             doc[token.i + 1].is_sent_start = True
#     return doc
#
#
# # Too bad implementation
# def create_train_data(text_file_dir, pos_file_dir):
#     text = open(text_file_dir).read()
#     pos = open(pos_file_dir).read()
#
#     nlp = spacy.load('en_core_web_sm')
#     nlp.add_pipe(set_custom_boundaries, before='parser')
#     nlp.max_length = 1200000
#
#     # Line-by-line sentences file
#     doc = nlp(text)
#     sentences = list(doc.sents)
#     file_sent = open('./created_files/sents_train.txt', 'w')
#     for sent in sentences:
#         sent_str = str(sent)
#         dot_end = sent_str.endswith(('.', '...', '?'))
#
#         if dot_end:
#             file_sent.write(sent_str + '\n')
#         else:
#             file_sent.write(sent_str + ' ')
#
#     file_sent.close()
#
#
#     # Line-by-line POS file
#     doc = nlp(pos)
#     pos_per_sents = list(doc.sents)
#
#     file_sent = open('./created_files/pos_train.txt', 'w')
#     for pos_sent in pos_per_sents:
#         pos_sent_str = str(pos_sent)
#         dot_end = pos_sent_str.endswith(('.', '...', '?'))
#
#         if dot_end:
#             file_sent.write(pos_sent_str + '\n')
#         else:
#             file_sent.write(pos_sent_str + ' ')
#     file_sent.close()
#
#
# # Convert parsed data for train
# # Example:
# # TRAIN_DATA = [
# #     ("I like green eggs", {"tags": ["N", "V", "J", "N"]}),
# #     ("Eat blue ham", {"tags": ["V", "J", "N"]}),
# # ]
# TRAIN_DATA = []
#
#
# def init_train_data(pos_train_file_path=None, sents_train_file_path=None):
#     if pos_train_file_path and sents_train_file_path:
#         with open(sents_train_file_path) as sents_file, open(pos_train_file_path) as pos_file:
#             for sent, pos in zip(sents_file, pos_file):
#                 sent = sent.strip()
#                 pos = pos.strip()
#
#                 TRAIN_DATA.append((sent, {"tags": pos.split()}))
#     else:
#         print('Incorrect paths')
#
#
# init_train_data('./created_files/pos_exp', './created_files/sents_exp')
# print(TRAIN_DATA)

# import re
#
# line = "``"
# line_1 = "u.s.a."
# print(re.match("^[a-zA-Z]+$", line_1))
# #print(re.search(r"[-!$%^&*()_+|~=`{}\[\]:\";'<>?,.\/]", line_1))


########################################################################################################################

# start_time = time.time()
# # text = open('./dataset/nyt_text.txt').read()
#
# text_len = len(text)
#
# def custom_tokenizer(nlp):
#     infixes = (
#         LIST_ELLIPSES
#         + LIST_ICONS
#         + [
#             r"(?<=[0-9])[+\-\*^](?=[0-9-])",
#             r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
#                 al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
#             ),
#             r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
#             #r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
#             r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
#         ]
#     )
#
#     infix_re = compile_infix_regex(infixes)
#
#     return Tokenizer(nlp.vocab, prefix_search=nlp.tokenizer.prefix_search,
#                                 suffix_search=nlp.tokenizer.suffix_search,
#                                 infix_finditer=infix_re.finditer,
#                                 token_match=nlp.tokenizer.token_match,
#                                 rules=nlp.Defaults.tokenizer_exceptions)
#
#
# nlp = spacy.load('en_core_web_sm')
# nlp.tokenizer = custom_tokenizer(nlp)
# nlp.max_length = 1500000
#
# # #################################################################
# # ###################### SET UP MATCHER ###########################
# # #################################################################
#
# matcher = Matcher(nlp.vocab)
#
# pattern = [{'ORTH': "'"},
#            {'ORTH': 've'}]
#
# pattern_2 = [{'ORTH': "'"},
#            {'ORTH': 'm'}]
#
# # pattern_3 = [{'LIKE_NUM': "True"},
# #              {'ORTH': '-'},
# #              {'LIKE_NUM': "True"}]
#
# matcher.add('QUOTED', None, pattern, pattern_2)
#
#
# def match_merger(doc):
#     # this will be called on the Doc object in the pipeline
#     matched_spans = []
#     matches = matcher(doc)
#     for match_id, start, end in matches:
#         span = doc[start:end]
#         matched_spans.append(span)
#     for span in matched_spans:  # merge into one token after collecting all matches
#         span.merge()
#     return doc
#
#
# nlp.add_pipe(match_merger, first=True)  # add it right after the tokenizer
# # #################################################################
#
# doc = nlp(text)
# elapsed_time = time.time() - start_time
#
# print(str(text_len) + ' characters were processed')
# print('Time spent: ' + str(elapsed_time) + 's')
########################################################################################################################


nlp = spacy.load('en_core_web_sm')
merge_ents = nlp.create_pipe("merge_entities")
merge_nps = nlp.create_pipe("merge_noun_chunks")
nlp.add_pipe(merge_nps, merge_ents)
matcher = Matcher(nlp.vocab)
Passive = "A camera is bought by him.\
            Water is drunk by her.\
            He is known to me.\
            A tub is filled with water.\
            Sugar is sold in kilograms.\
            There is a considerable range of expertise demonstrated by the spam senders.\
            It was determined by the committee that the report was inconclusive.\
            We were invited by our neighbors to attend their party.\
            Groups help participants realize that most of their problems and secrets are shared by others in the group.\
            The proposed initiative will be bitterly opposed by abortion rights groups.\
            Minor keys, modal movement, and arpeggios are shared by both musical traditions.\
            In this way, the old religion was able to survive the onslaught of new ideas until the old gods were finally displaced by Christianity.\
            First the apples are picked, then they are cleaned, and finally they’re packed and shipped to the market.\
            New York is considered the most diverse city in the U.S.\
            It is believed that Amelia Earhart’s plane crashed in Pacific Ocean.\
            Hungarian is seen as one of the world’s most difficult languages to learn.\
            Skin cancers are thought to be caused by excessive exposure to the sun.\
            George Washington was elected president in 1788.\
            Two people were killed in a drive-by shooting on Friday night.\
            Ten children were injured when part of the school roof collapsed.\
            I was hit by the dodgeball.\
            The metropolis has been scorched by the dragon’s fiery breath.\
            When her house was invaded, Penelope had to think of ways to delay her remarriage.\
            A new system of drug control laws was set up.\
            Heart disease is considered the leading cause of death in the United States.\
            The balloon is positioned in an area of blockage and is inflated.\
            The Exxon Company accepts that a few gallons might have been spilled.\
            100 votes are required to pass the bill.\
            Over 120 different contaminants have been dumped into the river.\
            Baby Sophia was delivered at 3:30 a.m. yesterday.\
            The letters are written by James.\
            The letters were written by James.\
            The letters are being written by James.\
            The letters have been written by James.\
            The letters are going to be written by James.\
            The letters will be written by James.\
            The letters were being written by James.\
            The cure had been found, but it was too late.\
            A cure will have been found by then.\
            Mistakes were made.\
            The butter is kept in the fridge.\
            My house is being kept tidy.\
            Mary's schedule was kept meticulously.\
            A seat was being kept for you.\
            All your old letters have been kept.\
            His training regimen had been kept up for a month.\
            The ficus will be kept.\
            If you told me, your secret would be kept.\
            Your bicycle would have been kept here if you had left it with me.\
            The book wants to be kept.\
            The puppy was happy to have been kept.\
            I have a feeling that a secret may be being kept.\
            The bird, having been kept in a cage for so long, might not survive in the wild.\
            The car can be sold by her every time.\
            Can a violin be played by her?\
            The house may be sold by him.\
            May the computer be bought by me?\
            The computer may not be bought by me.\
            His duty must be finished by him in a week.\
            The gate must not be opened by Dewi every morning.\
            Dewi might be met by him.\
            Chess might not be played guests.\
            At dinner, six shrimp were eaten by Harry.\
            The savannah is roamed by beautiful giraffes.\
            The flat tire was changed by Sue.\
            A movie is going to be watched by us tonight.\
            The obstacle course was run by me in record time.\
            The entire stretch of highway was paved by the crew.\
            The novel was read by Mom in one day.\
            A scathing review was written by the critic.\
            The house will be cleaned by me every Saturday.\
            A safety video will be watched by the staff every year.\
            The application for a new job was faxed by her.\
            The entire house was painted by Tom.\
            The students’ questions are always answered by the teacher.\
            That piece is really enjoyed by the choir.\
            By whom were you taught to ski?\
            The whole suburb was destroyed by the forest fire.\
            The treaty is being signed by the two kings.\
            Every night the office is vacuumed and dusted by the cleaning crew.\
            Money was generously donated to the homeless shelter by Larry.\
            My sales ad was not responded to by anyone.\
            All the reservations will be made by the wedding planner.\
            For the bake sale, two dozen cookies will be baked by Susan.\
            The comet was viewed by the science class.\
            The video was posted on Facebook by Alex.\
            Instructions will be given to you by the director.\
            The Grand Canyon is viewed by thousands of tourists every year.\
            The house was remodeled by the homeowners to help it sell.\
            The victory will be celebrated by the team tomorrow.\
            The metal beams were eventually corroded by the saltwater.\
            The baby was carried by the kangaroo in her pouch.\
            The last cookie was eaten by whom?\
            Tea is not liked by me.\
            The walls aren't painted by my mother.\
            The house is cleaned every day.\
            The house is being cleaned at the moment.\
            The house has been cleaned since you left.\
            The house was cleaned yesterday.\
            The house was being	cleaned	last week.\
            The house had been cleaned before they arrived.\
            The house will be cleaned next week.\
            The house will be being cleaned tomorrow.\
            The house would be cleaned if they had visitors.\
            The house would have been cleaned if it had been dirty.\
            The house must be cleaned before we arrive.\
            Dishes may be used, but they must not be left dirty in the sink.\
            What have you been given lately?\
            Have you or a friend ever been attacked or robbed? What happened?\
            What was done to it?\
            Who was it probably eaten by?"

# #Passive = "EBay Inc. said it agreed to sell its StubHub business to Geneva-based Viagogo Entertainment Inc. for $4.05 billion, a deal that would create a global ticketing giant in the booming live-events business.StubHub and smaller rival Viagogo are already among the largest players in the growing secondary market for sports, music and live-entertainment tickets, in which brokers and fans resell tickets purchased from primary vendors such as Live Nation Entertainment Inc.’s Ticketmaster."
# doc = nlp(Passive)
#
# # #####DEBUG LOOP####
# sents = list(doc.sents)
# file_debug = open('./debug_passive_voice.txt', 'w')
#
# passive_dep = ['nsubjpass', 'aux', 'auxpass', 'prt']
# matches = []
# for sent in doc.sents:
#     match = []
#     for token in sent:
#         if token.tag_ == 'VBN' and token.dep == 'ROOT' and token.text != 'been':
#             for child in token.children:
#                 if child.dep_ in passive_dep:
#                     match.append(child.text)
#             match.append(token.text)
#     file_debug.write(str(sent) + '\n')
#     file_debug.write(str(match) + '\n')
#     if match:
#         matches.append(match)
#
# file_debug.close()
#
# file_debug = open('./debug_passive_voice_matcher.txt', 'w')
# matcher = Matcher(nlp.vocab)
# text = Passive
# doc = nlp(text)
#
# print('Num of sents: ', len(list(doc.sents)))
# print('Dependency parse: ', len(matches))
# passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
# matcher.add('Passive', None, passive_rule)
# matches = matcher(doc)
#
# print('Matcher: ', len(matches))
# # for match in matches:
# #     print(doc[match[1]:match[2]])
#
# file_debug.close()
# displacy.serve(doc, style="dep")


doc = nlp("Tea is not liked by me.\
The house is cleaned every day.\
The house is being cleaned at the moment.\
The house has been cleaned since you left.\
The house was cleaned yesterday.\
The house was being	cleaned	last week.\
The house had been cleaned before they arrived.\
The house will be cleaned next week.\
The house will be being cleaned tomorrow.\
The house would be cleaned if they had visitors.\
The house would have been cleaned if it had been dirty.\
The house must be cleaned before we arrive.")
#
# doc = nlp(Passive)
# # for token in doc:
# #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
# #             token.shape_, token.is_alpha, token.is_stop)
# for sent in doc.sents:
#     for token in sent:
#         if token.tag_ == 'VBN' and token.dep_ == 'ROOT':
#             for child in token.children:
#                 print(child)
#
# sentence_spans = list(doc.sents)
# displacy.serve(sentence_spans, style="dep")

# tense_list = {
#         "PRESENT_SIMPLE":
#             dict(auxpass=["am", "is", "are"]),
#
#         "PRESENT_CONTINUOUS":
#             dict(aux=["am", "is", "are"], auxpass=["being"]),
#     }
#
# print(tense_list.get("PRESENT_SIMPLE").get('auxpass'))


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



text = "Dishes may be used, but they must not be left dirty in the sink."
text = "Who was it probably eaten by?\
        I was sucked into this internal U.S. fight.\
        Mr. Bondy, the lawyer for Mr. Parnas — who was arrested with Mr. Fruman last month on campaign finance-related charges and has signaled a willingness to cooperate with impeachment investigators — said in a statement that all of his client’s actions had been directed by Mr. Giuliani.\
        Mr. Parnas and Mr. Fruman flew to Tel Aviv to meet with Mr. Kolomoisky, who was seen as Mr. Zelensky’s patron.\
        For several years, Mr. Firtash’s most visible lawyer had been Lanny Davis, a well-connected Democrat who also represented Mr. Trump’s fixer-turned-antagonist, Michael Cohen. In a television appearance in March, Mr. Giuliani had attacked Mr. Davis for taking money from the oligarch, citing federal prosecutors’ contention that he was tied to a top Russian mobster — a charge Mr. Firtash has denied.\
        A document known as “Exhibit A” that was said to lay out the bribery scheme\
        Including the night before he was detained."

text = "By whom was this book written?\
        This book was written \
        Have they been invited by you?"
passive_phrases = passive_voice_search(text, 'ALL')
for phr in passive_phrases:
    print(phr)

text = Passive
doc = nlp(text)
sentence_spans = list(doc.sents)
# displacy.serve(sentence_spans, style="dep")

doc = nlp("I was sucked into this internal U.S. fight.")
print(len(doc))
for token in doc:
    print(token.text + " -> " + token.head.text)

passive_phrases = []
i = 0
while i < len(doc):
    token = doc[i]
    if token.dep_ == 'nsubjpass':
        passive_match = []
        for child in token.head.children:
            passive_match.append(child.text)
        passive_phrases.append(' '.join(passive_match))
        i = token.head.i + 1
    else:
        i += 1
print(passive_phrases)
# for i in range(doc)
# for token in sent:
#     if token.dep_ == 'nsubjpass':
#
#         passive_match = []
#         for child in token.head.children:
#             passive_match.append(child.text)
#         passive_phrases.append(' '.join(passive_match))
# displacy.serve(doc)
