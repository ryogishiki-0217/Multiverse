huggingface-cli download Multiverse4FM/Multiverse-32B --repo-type model --local-dir /cluster/home2/yueyang/Multiverse/Multiverse/model --local-dir-use-symlinks False 
huggingface-cli download Multiverse4FM/Multiverse-1K-mixed --repo-type dataset --local-dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts --local-dir-use-symlinks False 
python /cluster/home2/yueyang/Multiverse/Multiverse/inference/engine/Multiverse-Engine/example/example.py --model_path /cluster/home2/yueyang/Multiverse/Multiverse/model --prompts_dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download HuggingFaceH4/MATH-500 test.jsonl --repo-type dataset --local-dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/eval_src --local-dir-use-symlinks False 
huggingface-cli download simplescaling/aime24_figures aime24_figures.jsonl --repo-type dataset --local-dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/eval_src --local-dir-use-symlinks False 
huggingface-cli download opencompass/AIME2025 aime2025-II.jsonl --repo-type dataset --local-dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/eval_src --local-dir-use-symlinks False 
huggingface-cli download di-zhang-fdu/gpqa_diamond_multi_choice GPQA_DIAMOND_MC.json --repo-type dataset --local-dir /cluster/home2/yueyang/Multiverse/Multiverse/prompts/eval_src --local-dir-use-symlinks False
