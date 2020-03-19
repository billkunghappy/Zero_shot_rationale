import csv
import json
import string
import random
import sys
import random






###################args###############
#data_path
origin_data = 'reason_data.json'
output_path = sys.argv[1]

#random shuffle list?
random_list = True

#train/dev
# 260k: size = 229794
dev_rate = 0.1

#is_dev
is_dev = True

#data_num
data_num = int(sys.argv[2])
aspect_index = int(sys.argv[3])




# Questions
Question_apperance = 'How many points does the appearance of this beer get?'
Question_aroma = 'How many points does the aroma of this beer get?'
Question_palate = 'How many points does the palate of this beer get?'
Question_taste = 'How many points does the taste of this beer get?'
Question_total = 'How many points does this beer get?'
Question_list = [Question_apperance, Question_aroma, Question_palate, Question_taste, Question_total]

star = "This beer can get 1 points, 2 points, 3 points, 4 points, 5 points, 6 points, 7 points, 8 points, 9 points, 10 points in five aspects: appearance, aroma, palate, taste and total."
def multiple10(x):
    return 10*x



data = []


id = 0
cnt = 1
with open(origin_data, 'r') as ReadFile:
    F=json.load(ReadFile)
    for line in F:
        if cnt > data_num:
            break
        scores = line["score"]
        scores = [int(float(score)*10) for score in scores]
        star_score = []
        for score in scores:
            star_score.append( str(score)+' points' )
        #print('scores: ',scores, star_score)
        content = line["content"]
        

        # article
        article = {'title': 'Data_2_Title'}
        
        paragraphs = []
        
        context = {'context': star+' '+content}

        qas = []
        QANum = 5
        for QAcnt in range(QANum):
            if QAcnt != aspect_index:
                continue
            now_qa = {}
            now_answers = []

            AnswerNum = 1
            for Answercnt in range(AnswerNum):
                now_ans = {}
                now_ans['answer_start'] = context['context'].find(star_score[QAcnt])
                print(now_ans)
                now_ans['text'] = star_score[QAcnt]
            
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



train_data = {'data':data, 'version':'2.1'}

#print(root.keys())
with open(output_path, 'w') as output_file:
    json.dump(train_data, output_file)
        
print("File name: ",output_path)
print("data_num: ", data_num)
print("aspect_index: ",aspect_index )
print("Data_len: ", len(data)) 
        






















