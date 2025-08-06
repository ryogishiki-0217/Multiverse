# BEFORE RUN THIS SCRIPT, YOU NEED TO SET THE ROOT_DIR and GOOGLE_API_KEY

export GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

python models/gemini.py \
    --prompt $root_dir/data/prompt-step1.txt \
    --input $root_dir/data/1.1k.jsonl \
    --output $root_dir/data/output/step1/ \
    --chat $root_dir/data/output/step1/chat