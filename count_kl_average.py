import json

average_result = {}
for i in range(8):
	average_result[i] = {}

for i in range(8):
	for j in range(8):
		if i == j:
			average_result[i][j] = 0.0
		else:
			with open("Result_kl_divergence/kl_all/kl_divergence_" + str(i) + str(j) + ".json") as f_in:
				kl_all = json.load(f_in)

			sum = 0.0
			count = 0.0

			for id, value in kl_all.items():
				if type(value) == str:
					continue

				sum += value
				count += 1

			average_result[i][j] = sum / count

with open("Result_kl_divergence/kl_average/kl_average.json", "w") as f_out:
	json.dump(average_result, f_out)
