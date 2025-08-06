# BEFORE RUN THIS SCRIPT, YOU NEED TO SET THE ROOT_DIR

python src/data/preprocess.py \
    --input_dir_path $root_dir/data/output/step2/ \
    --output_dir_path $root_dir/data/output/step2/process/ \
    --ref_path $root_dir/data/1.1k.jsonl \
    --pattern s1

python src/data/parse.py \
    --input_file_path $root_dir/data/output/step2/process/ \
    --output_file_path $root_dir/data/output/step2/parse/ \
    --pattern s1

python src/data/afterwards.py \
    --input_file_path $root_dir/data/output/step2/process/ \
    --output_file_path $root_dir/data/output/step2/afterwards/ \
    --pattern s1

python src/data/distance.py \
    --input_file_path $root_dir/data/1.1k.jsonl \
    --output_file_path $root_dir/data/1.1k_multiverse.jsonl \
    --reasoning_dir $root_dir/data/output/step2/parse/ \
    --afterwards_dir $root_dir/data/output/step2/afterwards/ \
    --pattern s1 
