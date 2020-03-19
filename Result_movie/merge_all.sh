

dir='./withRats_pos'
output='pos_all.txt'


env rm -rf $output

all=`ls $dir`
for i in $all
do
	cat $dir/$i >> $output

done



