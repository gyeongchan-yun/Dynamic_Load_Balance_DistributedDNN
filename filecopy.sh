dbs=`pwd`

./scpall.sh ./filecopy.sh $dbs
./scpall.sh ./scpall.sh $dbs

./scpall.sh ./run_dbs_mp.sh $dbs
./scpall.sh ./dbs_mp.py $dbs
