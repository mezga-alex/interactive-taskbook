file = open('./dataset/test.txt', 'r')
file_pos = open('pos.txt', 'w')
file_text = open('text.txt', 'w')

for line in file:
    if len(line) > 1:
        file_pos.write(line.split()[1] + ' ')
        file_text.write(line.split()[0] + ' ')

file.close()
file_pos.close()
file_text.close()
