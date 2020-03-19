for i in {0..7}; do
		echo "start ${i}" >> dist_result.txt
		python3 cal_dist.py $i >> dist_result.txt;
done;
