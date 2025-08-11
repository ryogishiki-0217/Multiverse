import os
import re
from pathlib import Path

def extract_answers_from_file(file_path):
    """
    从GPQA结果文件中提取模型答案和参考答案
    返回格式: (model_answer, reference_answer)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取模型答案（匹配最后一个\boxed{}中的内容，确保括号匹配）
        # 使用正则表达式匹配\boxed{...}，支持嵌套括号
        start = content.rfind(r'\boxed{')
        if start == -1:
            model_answer = None
        start += len(r'\boxed{')  # 跳过 \boxed{
        balance = 0
        end = start
        # 遍历找到匹配的闭合 }
        for i in range(start, len(content)):
            if content[i] == '{':
                balance += 1
            elif content[i] == '}':
                balance -= 1
                if balance == 0:
                    end = i
                    break
    # 提取内容并替换 \dfrac 为 \frac
        extracted = content[start:end].strip()
        model_answer = extracted.replace(r'\dfrac', r'\frac')
        
        # 提取参考答案
        ref_match = re.search(r'参考答案: \s*(.*?)\s*$', content)
        reference_answer = ref_match.group(1) if ref_match else None
        print(model_answer)
        print(reference_answer)
        return model_answer, reference_answer
    
    except Exception as e:
        # 仅捕获异常，不打印错误信息
        return None, None

def calculate_accuracy(folder_path):
    """
    计算文件夹内所有GPQA结果文件的正确率，未找到模型答案或参考答案视为错误
    """
    total = 0
    correct = 0
    error_files = []  # 存储无法提取答案的文件
    
    # 遍历文件夹内所有txt文件
    for file in Path(folder_path).glob("*.txt"):
        total += 1
        model_ans, ref_ans = extract_answers_from_file(file)
        
        # 模型答案或参考答案缺失，视为错误
        if not model_ans or not ref_ans:
            error_files.append(file.name)
            continue
        
        if model_ans == ref_ans:
            correct += 1
            print(f"- {file}")
    # 计算正确率
    accuracy = correct / total if total > 0 else 0.0
    
    # 输出结果
    print(f"评估结果:")
    print(f"总文件数: {total}")
    print(f"正确数: {correct}")
    print(f"错误数: {total - correct}")  # 包含答案不匹配和提取失败的情况
    print(f"正确率: {accuracy:.2%}")
    
    if error_files:
        print(f"\n无法提取答案的文件 ({len(error_files)} 个):")

    return {
        "total": total,
        "correct": correct,
        "error": total - correct,
        "accuracy": accuracy,
        "error_files": error_files
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='评估GPQA结果文件夹的正确率')
    parser.add_argument('folder_path', help='包含GPQA结果txt文件的文件夹路径')
    args = parser.parse_args()
    
    calculate_accuracy(args.folder_path)