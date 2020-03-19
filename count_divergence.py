import json
import re
import torch
from torch.nn.functional import kl_div
from collections import OrderedDict
from transformers import *

def find_sublist(mylist, pattern):
	for i in range(len(mylist)):
		if mylist[i] == pattern[0] and mylist[i: i + len(pattern)] == pattern:
			return i
	return -1

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

with open("data_all.json") as f_all:
	data_all = json.load(f_all)

# ignore the contexts over max sequence length of BertTokenizer
re_mark = r"\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\\|\||\{|\[|\]|\}|\,|\<|\.|\>|\/|\?|\;|\:|\'|\""
encoded_contexts = [tokenizer.encode(data_all['data'][i]['paragraphs'][0]['context'].replace("[SEP]", " SEP "))
					if len(re.sub(re_mark, lambda x: ' ' + x.group() + ' ', data_all['data'][i]['paragraphs'][0]['context'].replace("[SEP]", " SEP ")).split()) < 512
					else None
					for i in range(len(data_all['data']))]

for i in range(8):
	with open("Result_change_label/nbest_CL_" + str(i) * 2 + ".json") as f_no_change:
		data_no_change = json.load(f_no_change)

	context_indexs = {}
	no_change_distributions = {}

	for id, results in data_no_change.items():
		if results[0]["text"] == "empty" and results[0]["probability"] == 1.0:
			context_indexs[id] = -1
			no_change_distributions[id] = None
		else:
			#encode the reason text and remove the mark of start and end
			encoded_result = tokenizer.encode(results[0]["text"])
			del encoded_result[0]
			del encoded_result[-1]

			found = False

			for index, encoded_context in enumerate(encoded_contexts):
				if encoded_context is not None and find_sublist(encoded_context, encoded_result) >= 0:
					context_indexs[id] = index
					original_distribution = [0.0] * len(encoded_context)

					for result in results:
						encoded_result = tokenizer.encode(result["text"])
						del encoded_result[0]
						del encoded_result[-1]
						result_index = find_sublist(encoded_context, encoded_result)

						for j in range(result_index, result_index + len(encoded_result)):
							original_distribution[j] += result["probability"]

					#smooth the distribution so that there would not be probability of 0
					original_distribution = torch.FloatTensor(original_distribution) + 1e-10
					original_distribution /= torch.norm(original_distribution, p = 1)
					no_change_distributions[id] = original_distribution
					found = True
					break

			if not found:
				context_indexs[id] = -2
				no_change_distributions[id] = None

	for j in range(8):
		if i == j:
			continue

		kl_result = {}

		with open("Result_change_label/nbest_CL_" + str(i) + str(j) + ".json") as f_change_label:
			data_change_label = json.load(f_change_label)

		for id, context_index in context_indexs.items():
			if context_index == -2:
				kl_result[id] = "Context over tokenizer max sequence length"
			elif context_index == -1:
				kl_result[id] = "Empty result"
			else:
				change_distribution = [0.0] * len(encoded_contexts[context_index])

				for result in data_change_label[id]:
					encoded_result = tokenizer.encode(result["text"])
					del encoded_result[0]
					del encoded_result[-1]
					result_index = find_sublist(encoded_contexts[context_index], encoded_result)

					for k in range(result_index, result_index + len(encoded_result)):
						change_distribution[k] += result["probability"]

				change_distribution = torch.FloatTensor(change_distribution) + 1e-10
				change_distribution /= torch.norm(change_distribution, p = 1)
				kl_result[id] = float(kl_div(change_distribution.log(), no_change_distributions[id]).numpy())

		final_kl_result = OrderedDict(sorted(kl_result.items(), key = lambda x: int(x[0])))

		with open("Result_kl_divergence/kl_all/kl_divergence_" + str(i) + str(j) + ".json", "w") as f_out:
			json.dump(final_kl_result, f_out)
