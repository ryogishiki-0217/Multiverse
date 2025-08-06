<div align="center">
<h1><img src="assets/multiverse-logo.png" height="40px" align="top"/> Multiverse Engine
</h1>

This repository contains the official implementation of **Multiverse Engine**,  which is built up from the [SGLang](https://github.com/sgl-project/sglang/tree/357fb2dba5543a3b40607ac43acc2582331b930c) codebase to support inference for **Multiverse Models**. For more details, please refer to our research paper: 
>[**Multiverse: Your Language Models Secretly Decide How to Parallelize and Merge Generation**](https://arxiv.org/abs/2506.09991)


</div>

## 🚀 Installation

To set up the environment, create a new conda environment and then run the following installation script.

```bash
conda create -n multiverse python=3.11
conda activate multiverse

git clone https://github.com/Multiverse4FM/Multiverse-Engine
cd Multiverse-Engine
bash install.sh
```


## ✨ Quick Start

The usage of Multiverse Engine is identical to the SGLang workflow. See `example.py` for a simple demonstration.

The script accepts the following arguments:
* `--model_path`: The path to the base model on your local machine or from the Hugging Face Hub.
* `--prompts_path`: A path to a JSON file containing a list of prompts.

To run the quick start example:

```bash
cd example

python example.py \
  --model_path Multiverse4FM/Multiverse-32B \
  --prompts_dir ./prompt
```

This will load the model and generate responses for each prompt in the specified text file, leveraging the Multiverse capabilities defined for the model.



## 🚧 Issues

We are actively working on addressing the following known issues and areas for improvement:

* [ ]  **Support KV Cache Eviction :**: Currently, KV cache offloading and reloading mechanisms are not supported. To ensure correctness, we recommend limiting the batch size to 50 or fewer.
* [ ]  **Avoid Infinite Parallelism**: We are working on implementing safeguards against infinite-depth parallelism that may be introduced by the model itself.

To avoid potential issues during usage, we recommend setting a maximum timeout in your code to prevent infinite loops or extremely long generation times.

## 📧 Contact

For any questions, bug reports, or feature requests, please open an issue on our [GitHub repository](https://github.com/Multiverse4FM/Multiverse-Engine/issues) or send an email to multiversefoundationmodel@gmail.com.

## 📚 References

Thank you for your interest in Multiverse Engine! We hope this tool will be helpful for your research and development. If you find it useful, please consider citing our work. Happy coding! 🚀

```bibtex
@misc{yang2025multiverselanguagemodelssecretly,
      title={Multiverse: Your Language Models Secretly Decide How to Parallelize and Merge Generation}, 
      author={Xinyu Yang and Yuwei An and Hongyi Liu and Tianqi Chen and Beidi Chen},
      year={2025},
      eprint={2506.09991},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2506.09991}, 
}
```