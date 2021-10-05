#!/bin/bash
echo "HOME:" $HOME
hostname=`hostname`
for i in 1 3 8 
do 
  server='shark'$i
  if [[ $hostname == $server ]]; then
    storage=/ssd_dataset/dataset
    container=pytorch
  fi
done

for i in 4 5 6 7
do 
  server='shark'$i
  if [[ $hostname == $server ]]; then
    storage=/ssd_dataset2/dataset
    container=pipedream
  fi
done

if [[ $hostname =~ 'tino' ]]; then
  storage=/hetpipe_ckpt
  container=pipedream_container
fi
echo $storage


nvidia-docker run -it -v $HOME:$HOME -v $storage:$storage --ipc=host --net=host $container /bin/bash
