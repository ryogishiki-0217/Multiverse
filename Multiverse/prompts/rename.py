import os
import json
import argparse

def rename_question_to_problem(json_dir):
    # 遍历目录中的所有文件
    for filename in os.listdir(json_dir):
        # 只处理JSON文件
        if filename.endswith('.json'):
            file_path = os.path.join(json_dir, filename)
            
            try:
                # 读取JSON文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 检查是否包含"question"字段
                if "question" in data:
                    # 将"question"字段重命名为"problem"
                    data["problem"] = data.pop("question")
                    
                    # 保存修改后的文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"已处理: {filename}")
                else:
                    print(f"跳过 {filename}: 未找到'question'字段")
            
            except json.JSONDecodeError:
                print(f"警告: {filename} 不是有效的JSON文件，已跳过")
            except Exception as e:
                print(f"处理 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将JSON文件中的'question'字段重命名为'problem'字段")
    parser.add_argument("--json_dir", type=str, required=True, help="包含JSON文件的目录路径")
    args = parser.parse_args()
    
    # 验证目录是否存在
    if not os.path.isdir(args.json_dir):
        print(f"错误: {args.json_dir} 不是一个有效的目录")
    else:
        rename_question_to_problem(args.json_dir)
        print("处理完成")
    