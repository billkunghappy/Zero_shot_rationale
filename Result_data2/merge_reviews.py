

output_file = 'data/reviews.all.train.txt'

file_list = ['data/reviews.aspect0.train.txt', 'data/reviews.aspect1.train.txt', 'data/reviews.aspect2.train.txt', 'data/reviews.aspect3.train.txt']
file_list.append('data/reviews.260k.train.txt')




s_all = set()


for file_name in file_list:
    print(file_name)
    with open(file_name, 'r') as read_file:
        
        while True:
            line = read_file.readline()
            if line == '':
                break
        
            if line not in s_all:
                s_all.add(line)

print(len(s_all))


with open()
for i in s_all:









