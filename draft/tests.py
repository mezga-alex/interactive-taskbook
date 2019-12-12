import text_processor
import pos_tagging
import passive_voice
import time

from globals import Passive, Active
import parse

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

if __name__ == "__main__":
    path = './dataset/train.txt'
    parse.parse_data('train', path)
    # path = './created_files/sents_exp.txt'
    # path = './dataset/nyt_text.txt'
    # text = text_processor.lexical_processor(open(path).read().lower())

    task = 'passive_voice'
    tense = 'ALL'
    pos = 'VBN'
    text = Passive
    if task == 'pos':
        pos_tagging.pos_tag_search(pos, text)

    if task == 'passive_voice':
        start_time = time.time()
        passive_phrases = passive_voice.passive_voice_search(text, tense)
        elapsed_time = time.time() - start_time
        print("tree single:", elapsed_time)

        start_time = time.time()
        passive_phrases_multi = passive_voice.passive_voice_search_multiprocessing(text, tense)
        elapsed_time = time.time() - start_time
        print("tree multi", elapsed_time)

        start_time = time.time()
        passive_phrases_matcher = passive_voice.matcher_passive_voice_search(text)
        elapsed_time = time.time() - start_time
        print("matcher:", elapsed_time)

    file_passive_tree = open('./created_files/passive_voice_tree.txt', 'w')
    file_passive_tree_multi = open('./created_files/passive_voice_tree_multi.txt', 'w')
    file_passive_matcher = open('./created_files/passive_voice_matcher.txt', 'w')
    for phr in passive_phrases:
        file_passive_tree.write(phr + "\n")
    for phr in passive_phrases_multi:
        file_passive_tree_multi.write(phr + "\n")
    for phr in passive_phrases_matcher:
        file_passive_matcher.write(phr + "\n")
    file_passive_tree.close()
    file_passive_tree_multi.close()
    file_passive_matcher.close()
