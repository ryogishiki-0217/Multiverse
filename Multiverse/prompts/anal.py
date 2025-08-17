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
        
        # 提取模型答案（匹配最后一个\boxed{}中的内容，正确处理嵌套括号）
        model_answer = None
        # 查找所有\boxed{的位置
        boxed_pattern = re.compile(r'\\boxed\{')
        matches = [m.start() for m in boxed_pattern.finditer(content)]
        
        if matches:
            # 取最后一个\boxed{的位置
            start_idx = matches[-1]
            # 从\boxed{开始计算完整括号范围
            balance = 0
            end_idx = -1
            # 包含\boxed{的起始位置开始遍历
            for i in range(start_idx, len(content)):
                if content[i] == '{':
                    balance += 1
                elif content[i] == '}':
                    balance -= 1
                    if balance == 0:
                        end_idx = i
                        break
            if end_idx != -1:
                # 提取完整的\boxed{...}字符串
                full_boxed = content[start_idx:end_idx+1]
                # 移除最外层的\boxed{和}
                extracted = full_boxed[len(r'\boxed{'):-1].strip()
                # 统一分数格式
                model_answer = extracted.replace(r'\dfrac', r'\frac')\
                                       .replace(r'\tfrac', r'\frac')\
                                       .replace(r'\cfrac', r'\frac')
        
        # 提取参考答案
        ref_match = re.search(r'参考答案:\s*(.*?)\s*(?=\n|$)', content, re.DOTALL)
        reference_answer = ref_match.group(1).strip() if ref_match else None
        #print(model_answer)
        #print(reference_answer)
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