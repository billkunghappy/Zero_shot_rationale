import csv
import json
import string
import random
import sys
import pickle


data_path = 'data/task2_trainset.csv'


QuestionNum = 1
MyQuestion = "The paper can ba labels as 8 types. Which type is this paper?"


QANum = 1
is_random = False
is_true= False
if sys.argv[1]=="random":
    is_random=True
if sys.argv[3]=="True":
    is_true=True
output_file_name = sys.argv[2]
if(output_file_name is None):
    print("please give ouput file name as argv[2]")

# Hierarchy
# root
##0: Dataset

##1: 
### "List"
#### "Association"
##### "Rule"
##### "Context"
##### 'Context'

##2: 
### 0:Typesystem Vector

##3:
### 0:Associastion

beginning_char = 46
Labels = "This paper can be labels as 8 types, THEORETICAL, EMPIRICAL, ENGINEERING, EMPIRICAL THEORETICAL, EMPIRICAL ENGINEERING, THEORETICAL ENGINEERING, EMPIRICAL THEORETICAL ENGINEERING, OTHERS."


### 001 -> THEORETICAL
### 010 -> EMPIRICAL
### 100 -> ENGINEERING
### 011 -> EMPIRICAL THEORETICAL
### 101 -> THEORETICAL ENGINEERING
### 110 -> EMPIRICAL ENGINEERING
### 111 -> EMPIRICAL THEORETICAL ENGINEERING

label_to_id = {"THEORETICAL": 1, "EMPIRICAL": 2, "ENGINEERING": 4, "OTHERS": 0}
id_to_label = {1: "THEORETICAL", 2: "EMPIRICAL", 4: "ENGINEERING", 3: "EMPIRICAL THEORETICAL", 5: "THEORETICAL ENGINEERING", 6: "EMPIRICAL ENGINEERING", 7: "EMPIRICAL THEORETICAL ENGINEERING", 0: "OTHERS"}



order = [1, 2, 4, 3, 5, 6, 7, 0]
label_position = {"THEORETICAL":37,"EMPIRICAL":50,"ENGINEERING":61,"EMPIRICAL THEORETICAL":74,"EMPIRICAL ENGINEERING":97,"THEORETICAL ENGINEERING":120,"EMPIRICAL THEORETICAL ENGINEERING":145,"OTHERS":180}
#tmp_pos = beginning_char
#for i in order:
#    tmp_pos += 2
#    now_label = id_to_label[i]
#    label_position[now_label] = answer_pos[i]
#    tmp_pos += len(now_label)



root = {}

data = []

#input data
with open('data/answers.pickle', 'rb') as file:
    answers =pickle.load(file)

with open('data/reason_text_prob.pickle', 'rb') as file:
    dat=pickle.load(file)
    text_list =dat['text']
    prob_list =dat['prob']

id = 0
with open(data_path, 'r') as csvFile:
    csvReader = csv.DictReader(csvFile)    
    

    cnt = 0
    wa=0
    for rows in csvReader:
        if cnt>=1000:
            break
        append=True
        article = {"title": rows['Title']}

        paragraphs = []

        paragraph_num = 1
        for i in range(paragraph_num):
            if is_random:
                random_len=len(text_list[cnt].split(" "))
                if random_len>=len(rows['Abstract'].split(" ")):
                    context = {"context": Labels+rows['Abstract']}
                else:
                    random_start=random.randint(0,len(rows['Abstract'].split(" "))-random_len)
                    random_replace=" ".join(rows['Abstract'].split(" ")[random_start:random_start+random_len])
                    if rows['Abstract'].find(random_replace)<0:
                        print('ERROR: cant find random')
                    random_context=rows['Abstract'].replace(random_replace," ".join(["[MASK]" for i in range(random_len)]))

                    if cnt==0:
                        print(random_context)
                    context = {"context": Labels+random_context}
            else:
                if rows['Abstract'].find(text_list[cnt])<0:
                    print('ERROR: cant find reason')
                masked_context=rows["Abstract"].replace(text_list[cnt]," ".join(["[MASK]" for i in range(len(text_list[cnt].split(" ")))]))
                context = {"context": Labels+masked_context}


            qas = []

            for j in range(QANum):
                now_qa = {}
                now_answers = []

                AnswerNum = 1
                for k in range(AnswerNum):
                    now_ans = {}
                    # Count Label
                    answer_id = 0
                    origin_answer_id=0

                    for __answers in rows['Task 2'].split():
                        origin_answer_id += label_to_id[__answers]

                    all_types={'EMPIRICAL':0,'THEORETICAL':0,"ENGINEERING":0,"OTHERS":0}
                    for __answers in answers[cnt].split():
                        __answers=__answers.replace(',','')
                        if all_types[__answers]==1:
                            continue
                        all_types[__answers]=1
                        answer_id += label_to_id[__answers]
                    if is_true and answer_id != origin_answer_id:
                        append=False
                    now_ans["answer_start"] = label_position[id_to_label[origin_answer_id]]
                    now_ans["text"] = id_to_label[origin_answer_id]
                
                    now_answers.append(now_ans)

                now_qa["answers"] = now_answers
                now_qa["question"] = MyQuestion
                #Now_ID = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24) ) 
                now_qa["id"] = str(id)
                id += 1
                
                qas.append(now_qa)

            context["qas"] = qas

            paragraphs.append(context)
        
        article["paragraphs"] = paragraphs
        if append is True:
            data.append(article)
        else:
            wa+=1
        cnt+=1
    print(wa)


root = {"data": data, "version": "1.1"}


with open(output_file_name, 'w') as jsonFile:
    json.dump(root, jsonFile)
























