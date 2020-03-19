import pickle
import json

with open("data/nbest_answer.json","r") as F:
    data=json.loads(F.read())
answer_list=[]
for i in range(1000):
    answer_list.append(data[str(i)][0]['text'])
with open("data/answers.pickle","wb") as F:
    pickle.dump(answer_list,F)
F.close()
