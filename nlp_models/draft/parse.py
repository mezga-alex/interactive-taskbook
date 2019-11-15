# #
# #
# # ##################################################################
# # ################        DANGEROUS, DON'T RUN!     ################
# # ################ MAGIC, NOBODY KNOWS HOW IT WORKS ################
# # ################   PLEASE, USE PARSED TXT FILES   ################
# # ##################################################################
# #
# #                 UPD: No, now it's quite OK

import string


# Plain text and POS-tags
def create_test_data(path):
    file = open(path, 'r')
    file_pos = open('./created_files/pos_test.txt', 'w')
    file_text = open('./created_files/text_test.txt', 'w')

    for line in file:
        if len(line) > 1:
            file_pos.write(line.split()[1] + ' ')
            file_text.write(line.split()[0] + ' ')

    file.close()
    file_pos.close()
    file_text.close()


# Line-by-line sentences and POS-Tags for them
def create_train_data(path):
    file_train = open(path, 'r')
    file_sent_line = open('./created_files/sents_train.txt', 'w')
    file_pos_line = open('./created_files/pos_train.txt', 'w')

    for f_line in file_train:
        if len(f_line) > 1:
            f_line = f_line.split()

            if f_line[1] not in string.punctuation and f_line[1] not in ("''", "``", "'", "`"):
                file_sent_line.write(f_line[0] + ' ')
                file_pos_line.write(f_line[1] + ' ')
            elif f_line[1] in ('.', '...', '?'):
                file_sent_line.write('\n')
                file_pos_line.write('\n')

    file_train.close()
    file_sent_line.close()
    file_pos_line.close()


# Count num of words in each line
# Return tuple (line_number, num_of_words)
def words_in_line(path):
    num_of_words = []
    i = 1
    file = open(path, 'r')
    for line in file:
        num_of_words.append((i, len(line.split())))
        i += 1
    file.close()
    return num_of_words


def find_difference(words_sents, words_pos):
    difference = []

    num_of_elements = len(words_pos)
    if len(words_sents) < num_of_elements:
        num_of_elements = len(words_sents)

    for i in range(num_of_elements):
        sent_num = words_sents[i][1]
        pos_num = words_pos[i][1]
        if sent_num != pos_num:
            difference.append((i + 1, pos_num, sent_num))
    return difference


def parse_data(dataset_type = 'train', trace = False):
    """
    Parse data from train or test files

    :param dataset_type: str - Select 'train' or 'test'
    :param trace: bool   - Select True to enable validation and print.

    """

    if dataset_type == 'train':
        dir_ = './dataset/train.txt'
        create_train_data(dir_)

        if trace:
            num_of_words_pos = words_in_line('./created_files/pos_train.txt')
            num_of_words_sents = words_in_line('./created_files/sents_train.txt')

            print('num_of_words_pos:')
            print(num_of_words_pos)
            print('num_of_words_sents')
            print(num_of_words_sents)

            diff = find_difference(num_of_words_sents, num_of_words_pos)
            print('find difference')
            print(diff)

    else:
        dir_ = './dataset/test.txt'
        create_test_data(dir_)

