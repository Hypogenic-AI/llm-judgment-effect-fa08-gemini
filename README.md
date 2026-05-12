# LLM Social Facilitation: The Judgment Effect

This project investigates how judgmental and skeptical tones affect LLM reasoning depth and quality.

## Key Findings
- **Social Facilitation confirmed**: LLMs (GPT-4o-mini) increase reasoning depth (by ~20%) when challenged with a judgmental tone.
- **Accuracy Boost**: judgmental framing improved social judgment accuracy by **6.6%** over neutral baselines.
- **Low Sycophancy**: Models maintained their logical convictions even under pressure, showing very low label flip rates (<7%).

## Project Structure
- `src/`: Core experimental scripts (`api_client.py`, `experiment_r_aio.py`, `experiment_causal.py`, `analyze_results.py`).
- `results/`: Raw output from experiments.
- `figures/`: Analysis plots.
- `REPORT.md`: Full research report with methodology and findings.

## How to Reproduce
1.  Setup environment: `uv venv && source .venv/bin/activate && uv pip install -r requirements.txt` (or install dependencies manually).
2.  Set `OPENAI_API_KEY`.
3.  Run experiments: `python src/experiment_r_aio.py` and `python src/experiment_causal.py`.
4.  Run analysis: `python src/analyze_results.py`.

## Full Report
See [REPORT.md](REPORT.md) for detailed analysis.
