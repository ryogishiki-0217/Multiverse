#!/bin/bash

#SBATCH -N 1
#SBATCH -p RTX3090
#SBATCH -w node01
#SBATCH --gres=gpu:4
#SBATCH -J Multiverse


CUDA_VISIBLE_DEVICES=1,2,3,8,9 python /cluster/home2/yueyang/Multiverse/Multiverse/inference/engine/Multiverse-Engine/example/eval.py --model_path /cluster/nvme2/yueyang/Multiverse/model --prompts_dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/MATH500_test --results_dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/MATH500_results --stats_dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/MATH500_acc