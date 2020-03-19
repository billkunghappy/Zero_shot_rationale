import pickle
import json

with open("data/nbest_reason.json","r") as F:
    data=json.loads(F.read())
text_list=[]
prob_list=[]
for i in range(1000):
    text_list.append(data[str(i)][0]['text'])
    prob_list.append(data[str(i)][0]['probability'])
print(text_list[0],prob_list[0])
text_prob_list={'text':text_list, 'prob': prob_list}
with open("data/reason_text_prob.pickle","wb") as F:
    pickle.dump(text_prob_list,F)
F.close()
