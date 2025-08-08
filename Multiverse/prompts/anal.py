import os
import re
from pathlib import Path
# 假设 math_grader.py 所在目录已在 PYTHONPATH 中
from grader import boxed_reward_fn

def extract_answer_and_gt(file_content):
    """
    从文件内容中提取模型输出的答案和参考答案
    返回格式: (model_answer_content, ground_truth)
    """
    # 提取模型输出内容（到"参考答案:"之前）
    model_output_match = re.split(r'参考答案:', file_content, flags=re.IGNORECASE)
    if len(model_output_match) < 2:
        return None, None
    model_output = model_output_match[0].strip()
    
    # 提取参考答案
    gt_match = re.split(r'是否正确:', model_output_match[1], flags=re.IGNORECASE)
    if len(gt_match) < 2:
        return model_output, None
    ground_truth = gt_match[0].strip()
    
    return model_output, ground_truth

def evaluate_txt_files(folder_path):
    """评估文件夹内所有txt文件的正确率"""
    total = 0
    correct = 0
    error_files = []
    
    # 遍历文件夹内所有txt文件
    for file in Path(folder_path).glob("*.txt"):
        total += 1
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取模型输出和参考答案
            model_output, ground_truth = extract_answer_and_gt(content)
            if not model_output or not ground_truth:
                error_files.append(f"{file.name} - 无法提取答案内容")
                continue
            
            # 使用 math_grader 中的评分函数进行评估
            # 这里使用 boxed_reward_fn，适用于带 \boxed{} 格式的答案
            info, reward = boxed_reward_fn(model_output, ground_truth, fast=False)
            
            if reward == 1.0:
                correct += 1
        
        except Exception as e:
            error_files.append(f"{file.name} - 处理错误: {str(e)}")
    
    # 计算正确率
    accuracy = correct / total if total > 0 else 0.0
    
    # 输出结果
    print(f"评估结果:")
    print(f"总文件数: {total}")
    print(f"正确数: {correct}")
    print(f"正确率: {accuracy:.2%}")
    
    if error_files:
        print("\n处理异常的文件:")
        for err in error_files:
            print(f"- {err}")
    
    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "errors": error_files
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='评估文件夹内txt文件的数学答案正确率')
    parser.add_argument('folder_path', help='包含txt文件的文件夹路径')
    args = parser.parse_args()
    
    evaluate_txt_files(args.folder_path)