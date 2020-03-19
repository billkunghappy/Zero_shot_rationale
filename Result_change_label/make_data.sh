for i in {0..7}; do
		for j in {0..7}; do
				python3 make_data.py reason data_CL_$i$j.json $i $j;
		done;
done;
