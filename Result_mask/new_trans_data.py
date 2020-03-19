import csv
import json
import string
import random
import sys



data_path = 'data/task2_trainset.csv'


QuestionNum = 1
MyQuestion = "The paper can ba labels as 8 types. Which type is this paper?"


QANum = 1
is_train = False
is_dev = False
is_reason = False
if sys.argv[1]=="train":
    is_train = True
elif sys.argv[1]=="dev":
    is_dev = True
elif sys.argv[1]=="reason":
    is_reason = True
    is_dev = True
else:
    print("please specified 'train' or 'dev' as argv[1]")

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

if is_reason:
    Labels = "This paper can be labels as 8 types. "
    MyQuestion = "The paper can ba labels as 8 types. Why is this paper be labeled as "
    #MyQuestion = "What is the subject of this paper. This paper can be labeled as "

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



id = 0
with open(data_path, 'r') as csvFile:
    csvReader = csv.DictReader(csvFile)    
    

    cnt = 0
    for rows in csvReader:
        if is_dev and (cnt >= 1000):
            break
        
        if is_train and (cnt<1000):
            cnt +=1
            continue

        article = {"title": rows['Title']}

        paragraphs = []

        paragraph_num = 1
        for i in range(paragraph_num):
            if is_reason:
                context = {"context": rows['Abstract']}
            else:
                context = {"context": Labels+rows['Abstract']}

            qas = []
            for j in range(QANum):
                now_qa = {}
                now_answers = []

                AnswerNum = 1
                for k in range(AnswerNum):
                    now_ans = {}
                    # Count Label
                    answer_id = 0
                    for __answers in rows['Task 2'].split():
                        answer_id += label_to_id[__answers]
                    if is_reason: 
                        now_ans["answer_start"] = 0
                        now_ans["text"] = "This"
                    else:
                        now_ans["answer_start"] = label_position[id_to_label[answer_id]]
                        now_ans["text"] = id_to_label[answer_id]
                    
                    now_answers.append(now_ans)

                now_qa["answers"] = now_answers
                if is_reason:
                    now_qa["question"] = MyQuestion + id_to_label[answer_id] + " ?"
                    #now_qa["question"] = MyQuestion + "XXXXXX" + " ?"
                else:
                    now_qa["question"] = MyQuestion
                #Now_ID = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24) ) 
                now_qa["id"] = str(id)
                id += 1
                
                qas.append(now_qa)

            context["qas"] = qas

            paragraphs.append(context)
        
        article["paragraphs"] = paragraphs
    
        data.append(article)
        cnt+=1



root = {"data": data, "version": "1.1"}


with open(output_file_name, 'w') as jsonFile:
    json.dump(root, jsonFile)
























