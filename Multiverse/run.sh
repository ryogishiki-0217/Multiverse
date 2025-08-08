#!/bin/bash

#SBATCH -N 1
#SBATCH -p RTX3090
#SBATCH -w node02
#SBATCH --gres=gpu:8
#SBATCH -J Multiverse


python /cluster/home2/yueyang/Multiverse/Multiverse/inference/engine/Multiverse-Engine/example/eval.py --model_path /cluster/nvme2/yueyang/Multiverse/model --prompts_dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/GPQA --results_dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/GPQA_results --stats_dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/GPQA_acc