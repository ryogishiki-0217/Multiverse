import json
import os

def extract_questions(input_file, output_dir="/cluster/home2/yueyang/Multiverse/Multiverse/prompts/GPQA"):
    """
    从输入的JSON文件中提取所有question条目，
    每条内容保存为一个独立的JSON文件
    
    参数:
        input_file: 输入的JSON文件路径
        output_dir: 保存输出文件的目录，默认为"extracted_questions"
    """
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 读取输入的JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 确保数据是一个列表
        if not isinstance(data, list):
            print("错误：输入文件内容不是一个列表")
            return
        
        # 处理每个条目
        for i, item in enumerate(data, 1):
            # 检查是否包含question字段
            if "question" in item:
                # 创建只包含question的字典
                question_data = {
                    "problem": item["question"],
                    "answer": item["answer"]
                    }
                # 生成文件名（使用序号）
                filename = f"question_{i}.json"
                output_path = os.path.join(output_dir, filename)
                
                # 写入JSON文件
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    json.dump(question_data, out_f, ensure_ascii=False, indent=2)
                
                print(f"已生成: {output_path}")
            else:
                print(f"警告：第{i}个条目不包含'question'字段，已跳过")
                
    except json.JSONDecodeError as e:
        print(f"JSON解析错误：{e}")
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except Exception as e:
        print(f"处理过程中出错：{e}")

if __name__ == "__main__":
    # 输入JSON文件路径（请替换为你的实际文件路径）
    input_json_file = "/cluster/home2/yueyang/Multiverse/Multiverse/prompts/eval_src/GPQA_DIAMOND_MC.json"
    
    # 提取并保存问题
    extract_questions(input_json_file)
    print("提取完成！")