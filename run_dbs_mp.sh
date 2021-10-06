#!/bin/bash

rank=$1
world_size=$2  # Number of nodes

if [ -z $rank ]; then
  echo "No rank error!"
  exit 1
fi
if [ -z $world_size ]; then
  echo "No world_size error!"
  exit 1
fi

#master=shark1
master=tino110
if [[ $rank == "0" ]] && [[ $world_size == "1" ]]; then
  master=`hostname`
  echo $master
  echo "Single node training!"
  exit 1;
fi

model=resnet34
batch_size=256 # Global size on a node
lr=0.01
gpu=0,1,2,3
dataset=cifar10
epochs=3
backend=nccl
log_dir=resnet34_1024_16_workers_nccl_logs/

echo "model: "$model "| batch size: "$batch_size "| gpu: "$gpu "| dataset: "$dataset
python dbs_mp.py \
  -dist-url 'tcp://'${master}':22000' \
  -dist-backend $backend \
  -ws $world_size \
  -rank $rank \
  -b $batch_size \
  -lr $lr \
  -m $model \
  -gpu $gpu \
  -ds $dataset \
  -e $epochs \
  -multiprocessing-distributed \
  -log-dir $log_dir
