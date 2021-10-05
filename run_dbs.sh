#!/bin/bash

model=densenet
batch_size=128 # Global size on a node
gpu=0,1,2,3
world_size=4
dataset=cifar10

echo "model: "$model "| batch size: "$batch_size "| gpu: "$gpu "| dataset: "$dataset
python dbs.py \
  -ws $world_size \
  -b $batch_size \
  -m $model \
  -gpu $gpu \
  -ds $dataset
