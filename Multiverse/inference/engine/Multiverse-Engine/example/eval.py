import os
import json
import argparse
import shutil
from transformers import AutoTokenizer
import sglang as sgl

def main(args):
    # 设置后端并初始化模型引擎
    sgl.set_default_backend("vllm")
    model_path = args.model_path
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    llm = sgl.Engine(
        model_path=model_path,
        tp_size=2,
        log_level="info",
        disable_overlap_schedule=True
    )
    
    # 创建结果保存目录（如果不存在）
    if os.path.exists(args.results_dir):
        shutil.rmtree(args.results_dir)  # 清空现有结果目录
    os.makedirs(args.results_dir, exist_ok=True)
    
    # 定义会话处理函数（每个文件单独处理）
    def process_single_file(file_path):
        # 读取JSON文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 提取问题和参考答案
        math_question = data.get("problem", "")
        reference_answer = data.get("answer", "").strip().lower()
        
        # 构建格式化提示词，增加固定结束语要求
        system_prompt = """You are Qwen, created by Alibaba Cloud. You are a helpful assistant specializing in solving math problems.
When solving math problems, please show your reasoning process first, then provide the final answer in a fixed format:
"the final answer is ..."
Replace ... with the actual answer. Ensure this exact phrase is included at the end of your response."""
        
        formatted_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\nSolve the following math problem: {math_question}\n<|im_end|>\n<|im_start|>assistant\n"
        
        # 采样参数
        sampling_params = {
            "temperature": 0.6,
            "top_p": 0.95,
            "max_new_tokens": 8000,
            "skip_special_tokens": False,
            "stop_token_ids": [151670, 151674]
        }
        
        # 单独生成（每个文件一个会话）
        output = llm.generate(formatted_prompt, sampling_params)
        output_text = output['text']
        
        # 提取最终答案（基于固定结束语）
        final_answer = None
        answer_marker = "the final answer is "
        marker_index = output_text.lower().find(answer_marker)
        
        if marker_index != -1:
            final_answer = output_text[marker_index + len(answer_marker):].strip()
            # 移除可能的标点符号并标准化
            final_answer = final_answer.rstrip('.').rstrip('!').rstrip('?').lower()
        
        # 判断答案是否正确
        is_correct = False
        if final_answer and reference_answer:
            # 简单比对，可根据需要扩展更复杂的比对逻辑
            is_correct = final_answer == reference_answer
        
        # 输出结果到控制台
        print("===============================")
        print(f"处理文件: {os.path.basename(file_path)}")
        print(f"问题: {math_question}")
        print(f"模型解答: {output_text}")
        print(f"提取的答案: {final_answer if final_answer else '未找到符合格式的答案'}")
        print(f"参考答案: {reference_answer}")
        print(f"是否正确: {'是' if is_correct else '否'}")
        
        # 计算生成比例
        gen_token_count = len(tokenizer.encode(output_text))
        ratio = gen_token_count / sampling_params['max_new_tokens']
        print(f"生成比例: {ratio:.4f}")
        print("===============================\n")
        
        # 保存结果到TXT文件
        txt_filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
        txt_path = os.path.join(args.results_dir, txt_filename)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"问题: {math_question}\n\n")
            f.write(f"模型解答: {output_text}\n\n")
            f.write(f"提取的答案: {final_answer if final_answer else '未找到符合格式的答案'}\n\n")
            f.write(f"参考答案: {reference_answer}\n\n")
            f.write(f"是否正确: {'是' if is_correct else '否'}\n")
        
        return {
            "filename": os.path.basename(file_path),
            "final_answer": final_answer,
            "reference_answer": reference_answer,
            "is_correct": is_correct
        }

    # 遍历文件夹下的所有JSON文件并逐个处理
    results = []
    total_count = 0
    correct_count = 0
    
    for filename in os.listdir(args.prompts_dir):
        if filename.endswith(".json"):  # 只处理JSON文件
            file_path = os.path.join(args.prompts_dir, filename)
            if os.path.isfile(file_path):
                result = process_single_file(file_path)
                results.append(result)
                total_count += 1
                if result["is_correct"]:
                    correct_count += 1
    
    # 计算正确率
    accuracy = correct_count / total_count if total_count > 0 else 0.0
    
    # 保存统计结果
    stats = {
        "total": total_count,
        "correct": correct_count,
        "accuracy": accuracy,
        "accuracy_percent": f"{accuracy * 100:.2f}%",
        "results": results
    }
    
    # 保存详细统计到JSON
    stats_json_path = os.path.join(args.stats_dir, "evaluation_stats.json")
    with open(stats_json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    # 保存简洁统计到TXT
    stats_txt_path = os.path.join(args.stats_dir, "evaluation_summary.txt")
    with open(stats_txt_path, "w", encoding="utf-8") as f:
        f.write(f"总问题数: {total_count}\n")
        f.write(f"正确数: {correct_count}\n")
        f.write(f"正确率: {accuracy * 100:.2f}%\n")
    
    print(f"评估完成！总问题数: {total_count}, 正确数: {correct_count}, 正确率: {accuracy * 100:.2f}%")
    print(f"详细结果保存在: {args.results_dir}")
    print(f"统计信息保存在: {args.stats_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True, help="Path to the Multiverse model")
    parser.add_argument("--prompts_dir", type=str, required=True, help="Path to the directory containing JSON math problems")
    parser.add_argument("--results_dir", type=str, default="./results", help="Directory to save individual results")
    parser.add_argument("--stats_dir", type=str, default="./stats", help="Directory to save accuracy statistics")
    args = parser.parse_args()
    
    # 创建统计目录（如果不存在）
    os.makedirs(args.stats_dir, exist_ok=True)
    
    main(args)
    