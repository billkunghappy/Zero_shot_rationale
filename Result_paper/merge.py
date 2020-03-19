import csv
import json
import string
import random
import sys




data_path = sys.argv[1]
SQuAD_path = sys.argv[2]

json_path = sys.argv[3]

#shuffle
is_shuffle = True



with open(data_path, 'r') as F1:
    a = json.load(F1)

with open(SQuAD_path, 'r') as F2:
    b = json.load(F2)




merged_list = a['data']+b['data']

if is_shuffle:
    random.shuffle(merged_list)

merged_dict = {'version': a['version'], 'data': merged_list}


with open(json_path, 'w') as F3:
    json.dump(merged_dict, F3)








