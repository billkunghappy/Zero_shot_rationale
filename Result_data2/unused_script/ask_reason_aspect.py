import csv
import json
import string
import random
import sys
import re


data_path = 'annotations.json'
target_path = sys.argv[1]
random_list = False
data_num = int(sys.argv[2])
aspect_index= int(sys.argv[3])

# aspect
# appearance, aroma, palate, taste, total


def get_question(score, aspect):
    print(score)
    nowq = 'Why does this beer get '+str(score)+' points in the aspect of '+str(aspect)+'?'
    return nowq

aspect_list = ['appearance', 'aroma', 'palate', 'taste', 'overall']
    
data = []


root = {}

id = 0


cnt = 1

with open(data_path, 'r') as jsonFile:
    for lines in jsonFile:
        if lines is None:
            break
        if cnt > data_num:
            break
        jrow = json.loads(lines)
        
        raw = json.dumps(eval(jrow['raw']))
        raw = json.loads(raw)
        score = jrow['y'] 
        # print(raw.keys())
        #/input()
        comments = {}
        ###### the title 
        article = {"title": 'Data2_Reason'}
        paragraphs = []
        paragraph_num = 1
               
        
        for i in range(paragraph_num):
            context = {"context": raw['review/text']}
            
            qas = []
            # each annotation -> one QA.
                        
            for index in range(5):
                if index != aspect_index:
                    continue
                # print('id:', index)
                for now_answer in jrow[str(index)] :
                    # print(now_answer)
                    now_qa = {}
                    now_answers = []
                    # print(' '.join(str(tmp_list[x]) for x in range(now_answer[0], now_answer[1])))
                
                    tmp_list = jrow['x'][now_answer[0]:now_answer[1]]
                    #print('tmp_list', tmp_list)

                    tmp_str = (' ').join(str(x) for x in tmp_list)
                    total_str = (' ').join(str(x) for x in jrow['x'])


                    #print('tmp_str', tmp_str)
                    
                    now_ans = {}

                    # ANS start
                    now_ans['answer_start'] = total_str.find(tmp_str)
                    print('now_ans', now_ans)
                    now_ans['text'] = tmp_str

                    now_answers.append(now_ans)
                    # print('now_answers', now_answers)

                now_qa['answers'] = now_answers
                now_qa['id'] = str(id)
                nowas = aspect_list[index]
                # print(nowas)
                now_qa['question'] = get_question(int(score[index]*10), nowas)
                # print(now_qa['question'])
                # input()
    
                qas.append(now_qa)
                id += 1
                
            context['qas'] = qas

            paragraphs.append(context)
    
        article['paragraphs'] = paragraphs
        
        # print(article)
        data.append(article)
        
        cnt += 1

            
if random_list == True:
    random.shffle(data)

print(len(data))

root = {'data': data, 'version': '2.2'}
with open(target_path, 'w') as output_file:
    json.dump(root, output_file)

                



