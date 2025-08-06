# BEFORE RUN THIS SCRIPT, YOU NEED TO SET THE ROOT_DIR

export GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

python models/refill_block.py \
    --input $root_dir/data/1.1k.jsonl \
    --output_xml $root_dir/data/output/step3/ \
    --xml_path $root_dir/data/output/step2/parse