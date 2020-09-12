#!/bin/bash

dir=$1
length=$2
balanced=$3

python input_creation_pipeline.py \
        --dir $dir \
        --length $length

python categorical_neural_network.py \
        --dir $dir \
	--length $length \
        --balanced $balanced
