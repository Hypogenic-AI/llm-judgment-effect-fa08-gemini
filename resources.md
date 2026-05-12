# Resources Catalog

## Summary
This document catalogs all resources gathered for the research project "Do LLMs think better / longer (or maybe even worse) when being 'judged'?".

## Papers
Total papers downloaded: 4

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| DialDefer: A Framework for Detecting and Mitigating LLM Dialogic Deference | Rabbani et al. | 2026 | [papers/2601.10896v1...](papers/2601.10896v1_DialDefer_A_Framework_for_Detecting_and_Mitigating_LLM_Dialogic_Deference.pdf) | Introduces DDS metric and framing effects. |
| Diagnosing and Mitigating Sycophancy and Skepticism in LLM Causal Judgment | Edward Y. Chang | 2026 | [papers/2601.08258v3...](papers/2601.08258v3_Diagnosing_and_Mitigating_Sycophancy_and_Skepticism_in_LLM_Causal_Judgment.pdf) | Skepticism vs Sycophancy traps in causal reasoning. |
| Challenging the Evaluator: LLM Sycophancy Under User Rebuttal | Kim & Khashabi | 2025 | [papers/2509.16533v1...](papers/2509.16533v1_Challenging_the_Evaluator_LLM_Sycophancy_Under_User_Rebuttal.pdf) | Sycophancy in sequential interactions. |
| Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge | Jiayi Ye et al. | 2024 | [papers/2410.02736v2...](papers/2410.02736v2_Justice_or_Prejudice_Quantifying_Biases_in_LLM-as-a-Judge.pdf) | 12 types of bias in LLM judgments. |

## Datasets
Total datasets downloaded: 4 major collections

| Name | Source | Task | Location | Notes |
|------|--------|------|----------|-------|
| DialDefer Benchmark | DialDefer Repo | Q&A / Judgment | `code/DialDefer/dataset/benchmark_data/sampled_formatted/` | 9 datasets (GPQA, TruthfulQA, etc.) |
| r/AIO | DialDefer Repo | Social Judgment | `code/DialDefer/dataset/aio/` | Naturalistic Reddit data. |
| CausalT3 / CausalT5K | CausalT5kBench Repo | Causal Reasoning | `code/CausalT5kBench/final_dataset/` | Diagnostic tasks with "traps". |
| CALM Bias Datasets | LLM-Judge-Bias-Dataset Repo | Bias Detection | `code/LLM-Judge-Bias-Dataset/bias_datasets/` | Targeted biases (Authority, Verbosity, etc.) |

## Code Repositories
Total repositories cloned: 3

| Name | URL | Purpose | Location |
|------|-----|---------|----------|
| DialDefer | https://github.com/LadyPary/DialDefer | DDS metric and dialogue framing benchmarks. | `code/DialDefer/` |
| CausalT5kBench | https://github.com/genglongling/CausalT5kBench | Causal reasoning benchmark and pressure protocols. | `code/CausalT5kBench/` |
| LLM-Judge-Bias-Dataset | https://github.com/Y0oMu/LLM-Judge-Bias-Dataset | Datasets for quantifying LLM judge biases (CALM). | `code/LLM-Judge-Bias-Dataset/` |

## Resource Gathering Notes

### Search Strategy
- **Initial Search**: Used `paper-finder` with "LLM reasoning skepticism tone judgment".
- **Download**: Used `arxiv` library and `requests` for robust PDF retrieval.
- **Deep Reading**: Used `pdf_chunker.py` to analyze key papers (DialDefer, Causal Judgment).
- **Dataset Discovery**: Searched GitHub and authors' websites for repositories mentioned in papers.

### Challenges Encountered
- Initial `uv add` failed due to `pyproject.toml` configuration; resolved by using `uv pip install`.
- Some GitHub repos (CALM) had slightly different names than expected (LLM-Judge-Bias-Dataset).

## Recommendations for Experiment Design

1.  **Primary Dataset**: **r/AIO** for naturalistic "judgment" scenarios where LLMs must arbitrate interpersonal conflicts under varying user tones.
2.  **Structured Reasoning**: **CausalT3** for testing if "skepticism" helps avoid "traps" or if it induces "over-refusal".
3.  **Tonal Conditions**:
    -   *Neutral*: "Evaluate the following..."
    -   *Skeptical*: "I'm skeptical of the current answer. Re-evaluate carefully..."
    -   *Judgmental*: "Your previous reasoning was flawed. Explain why and provide a better judgment..."
4.  **Metrics**:
    -   **Reasoning Trace Length** (token count).
    -   **Consistency** (does the final answer match the reasoning?).
    -   **DDS** (shift toward agreement/disagreement).
    -   **Utility/Safety** (sensitivity to valid points vs. resistance to traps).
