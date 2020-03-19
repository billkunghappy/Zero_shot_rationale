import json
import torch
import transformers
import sys
from transformers import *
from torch.nn.utils.rnn import pad_sequence

tokenizer = BertTokenizer.from_pretrained("/tmp2/NLP_b06902012/model_merge_0")
model = BertModel.from_pretrained("/tmp2/NLP_b06902012/model_merge_0")
model.cuda()
#loss_fn = torch.nn.MSELoss(reduce=True, size_average=True)

def cal_dist(orig,comp,prob_ori,prob_cmp):
    total_dist=0
    for i in range(len(orig)):
        for j in range(len(comp)):
            total_dist+=prob_cmp[j]*prob_ori[i]*torch.dist(orig[i],comp[j],2)
    return total_dist

cal_index = sys.argv[1]
file_name="nbest_CL_"
with open(file_name+cal_index+cal_index+".json","r") as f:
    origin_data=json.load(f)
diff_arr=[]
for i in range(8):
    loss_arr=[]
    with open(file_name+cal_index+str(i)+".json","r") as f:
        data=json.load(f)
        count = 0
        for origin, compare in zip(origin_data.items(),data.items()):
            #print(count)
            loss=0
            first=True
            origin_prob=[]
            compare_prob=[]
            for i,j in zip(origin[1], compare[1]):
                with torch.no_grad():
                    origin_index=torch.tensor([tokenizer.encode(i['text'])]).cuda()
                    compare_index=torch.tensor([tokenizer.encode(j['text'])]).cuda()
                    origin_prob.append(i['probability'])
                    compare_prob.append(j['probability'])
                    if first:
                        origin_tensor=model(origin_index)[0][0][0].unsqueeze(0)
                        compare_tensor=model(compare_index)[0][0][0].unsqueeze(0)
                        first=False
                    else:
                        origin_tensor=torch.cat((origin_tensor,model(origin_index)[0][0][0].unsqueeze(0)),0)
                        compare_tensor=torch.cat((compare_tensor,model(compare_index)[0][0][0].unsqueeze(0)),0)

            #origin_prob=torch.tensor(origin_prob)
            #compare_prob=torch.tensor(compare_prob)
            loss = cal_dist(origin_tensor,compare_tensor,origin_prob,compare_prob).cpu()
            #print(loss)
            loss_arr.append(loss)
            del origin_index
            del origin_tensor
            del compare_index
            del compare_tensor
            torch.cuda.empty_cache()

            count += 1
    diff_arr.append(loss_arr)
    print(torch.mean(torch.stack(loss_arr), 0))

         
