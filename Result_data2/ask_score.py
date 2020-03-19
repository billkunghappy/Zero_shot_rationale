import csv
import json
import string
import random
import sys
import random




###################args###############
#data_path
origin_data = sys.argv[1]
output_path = sys.argv[2]
dev_path = sys.argv[3]

#random shuffle list?
random_list = True

#train/dev
# 260k: size = 229794

#is_dev
is_dev = True

#data_num
train_size = int(sys.argv[4])

#dev_num
dev_size = int(sys.argv[5])


data_num = train_size+dev_size



# Questions
Question_appearance = 'How is this beer rated by this comment in the aspect of appearance?'
Question_aroma = 'How is this beer rated by this comment in the aspect of aroma?'
Question_palate = 'How is this beer rated by this comment in the aspect of palate?'
Question_taste = 'How is this beer rated by this comment in the aspect of taste?'
Question_total = 'How is this beer rated by this comment in the aspect of total?'
#Question_total = 'How many points does this beer get?'
Question_list = [Question_appearance, Question_aroma, Question_palate, Question_taste, Question_total]

star = "This beer can be rated as bad, medium, good in five aspects: appearance, aroma, palate, taste and total."



data = []
def score_to_rate(score):
    if score < 0.4:
        return "bad"
    elif score < 0.8:
        return "medium"
    else:
        return "good"

id = 0
cnt = 1
with open(origin_data, 'r') as ReadFile:
    
    while True:
        if cnt > data_num:
            break

        line = ReadFile.readline()        
        # print(line, end='')
        if line == '':
            break

        line = line.split('\t')
        scores = line[0]
        scores = scores.split(' ')
        rates = [score_to_rate(float(score)) for score in scores]
        #print('scores: ',scores, star_score)
        content = line[1]
        

        # article
        article = {'title': 'Data_2_Title'}
        
        paragraphs = []
        
        context = {'context': star+' '+content}

        qas = []
        QANum = 5
        for QAcnt in range(QANum):
            now_qa = {}
            now_answers = []

            AnswerNum = 1
            for Answercnt in range(AnswerNum):
                now_ans = {}
                now_ans['answer_start'] = context['context'].find(rates[QAcnt])
                print(now_ans)
                now_ans['text'] = rates[QAcnt]
            
                now_answers.append(now_ans)


            now_qa['answers'] = now_answers
            now_qa['question'] = Question_list[QAcnt]

            now_qa['id'] = str(id)
            id += 1

            qas.append(now_qa)
        
            context['qas'] = qas
        
        paragraphs.append(context)
        
        article['paragraphs'] = paragraphs
        data.append(article)
        cnt += 1
                
        #input()


if random_list == True:
    random.shuffle(data)

print(len(data))


train_data = data[:train_size]
dev_data = data[train_size:]
print(len(train_data), len(dev_data))

train_root = {'data':train_data, 'version':'2.1'}
if is_dev: 
    dev_root = {'data':dev_data, 'version':'2.1'}

#print(root.keys())
with open(output_path, 'w') as output_file:
    json.dump(train_root, output_file)
        
if is_dev:
    with open(dev_path, 'w') as dev_file:
        json.dump(dev_root, dev_file)
        
        
        
        






















