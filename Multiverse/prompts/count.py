import os
import re
from pathlib import Path


def calculate_accuracy(folder_path):
    """
    计算文件夹内所有GPQA结果文件的正确率，未找到模型答案或参考答案视为错误
    """
    total = 0
    correct = 0
    error_files = []  # 存储无法提取答案的文件
    
    # 遍历文件夹内所有txt文件
    for file in Path(folder_path).glob("*.json"):
        total += 1

    print(f"总文件数: {total}")


    return {
        "total": total
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='评估GPQA结果文件夹的正确率')
    parser.add_argument('folder_path', help='包含GPQA结果txt文件的文件夹路径')
    args = parser.parse_args()
    
    calculate_accuracy(args.folder_path)