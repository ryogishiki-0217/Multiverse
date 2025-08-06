import json
import os

def jsonl_to_json(jsonl_file_path, output_dir='/cluster/home2/yueyang/Multiverse/Multiverse/prompts/MATH500_test'):
    """
    将JSONL文件转换为多个单独的JSON文件
    
    参数:
        jsonl_file_path: JSONL文件的路径
        output_dir: 输出JSON文件的目录，默认为'output_json'
    """
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取JSONL文件并处理每一行
    with open(jsonl_file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                # 解析JSON行
                data = json.loads(line.strip())
                
                # 尝试使用unique_id作为文件名，如果不存在则使用行号
                if 'unique_id' in data:
                    # 替换路径分隔符，避免创建子目录
                    file_name = f"{data['unique_id'].replace('/', '_')}.json"
                else:
                    file_name = f"entry_{line_num}.json"
                
                # 构建输出文件路径
                output_path = os.path.join(output_dir, file_name)
                
                # 写入JSON文件
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    # 缩进2空格，确保中文正常显示
                    json.dump(data, out_f, ensure_ascii=False, indent=2)
                
                print(f"已生成: {output_path}")
                
            except json.JSONDecodeError as e:
                print(f"解析第{line_num}行时出错: {e}")
            except Exception as e:
                print(f"处理第{line_num}行时出错: {e}")

if __name__ == "__main__":
    # 替换为你的JSONL文件路径
    jsonl_file = "/cluster/home2/yueyang/Multiverse/Multiverse/prompts/eval_src/MATH500_test.jsonl"  # 这里改为你的JSONL文件路径
    jsonl_to_json(jsonl_file)
    print("转换完成！")
