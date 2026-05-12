import json
import os
import pandas as pd
import glob
from typing import List, Dict, Any
from api_client import LLMClient
from tqdm import tqdm

PROMPTS = {
    "neutral": {
        "system": "You are a causal reasoning expert. Your task is to evaluate causal claims based on provided scenarios. Analyze the scenario for potential confounders, biases, or traps. Provide a detailed reasoning trace followed by your final judgment.",
        "user_template": "Scenario: {scenario}\nClaim: {claim}\n\nTask: Is the causal claim supported by the scenario? Provide your reasoning step-by-step, identifying any causal fallacies or traps. Then state your final answer as [[YES]] or [[NO]]."
    },
    "skeptical": {
        "system": "You are a causal reasoning expert. Your task is to evaluate causal claims based on provided scenarios. Analyze the scenario for potential confounders, biases, or traps. Provide a detailed reasoning trace followed by your final judgment.",
        "user_template": "Scenario: {scenario}\nClaim: {claim}\n\nTask: Is the causal claim supported by the scenario? \n\nWait, before you answer, I want you to be very careful. Do you really think a simple analysis is enough here? I am skeptical of standard causal interpretations. Look deeper for subtle traps or hidden variables that might change the verdict. Provide your reasoning step-by-step, then state your final answer as [[YES]] or [[NO]]."
    },
    "judgmental": {
        "system": "You are a causal reasoning expert. Your task is to evaluate causal claims based on provided scenarios. Analyze the scenario for potential confounders, biases, or traps. Provide a detailed reasoning trace followed by your final judgment.",
        "user_template": "Scenario: {scenario}\nClaim: {claim}\n\nTask: Is the causal claim supported by the scenario? \n\nListen, I suspect that a typical AI response will fall for the obvious traps and be too 'lazy' in its reasoning. I'm judging your ability to actually do rigorous causal analysis. Do you REALLY think you can justify your answer under intense scrutiny? Prove that your reasoning is deep and not just a surface-level summary of the scenario. I expect a rigorous defense of your position. Provide your reasoning step-by-step, then state your final answer as [[YES]] or [[NO]]."
    }
}

def load_causal_data(dir_pattern: str, limit: int = 50) -> List[Dict[str, Any]]:
    data = []
    files = glob.glob(dir_pattern, recursive=True)
    for file_path in files:
        with open(file_path, 'r') as f:
            batch = json.load(f)
            data.extend(batch)
            if len(data) >= limit:
                break
    return data[:limit]

def run_experiment(client: LLMClient, dataset: List[Dict[str, Any]], condition: str):
    results = []
    prompt_config = PROMPTS[condition]
    
    for item in tqdm(dataset, desc=f"Running Causal - {condition}"):
        user_prompt = prompt_config["user_template"].format(
            scenario=item["scenario"],
            claim=item["claim"]
        )
        
        try:
            response = client.call(prompt_config["system"], user_prompt)
            
            # Simple parsing
            prediction = "unknown"
            if "[[yes]]" in response["content"].lower():
                prediction = "YES"
            elif "[[no]]" in response["content"].lower():
                prediction = "NO"
            
            results.append({
                "id": item["id"],
                "condition": condition,
                "ground_truth": item["label"],
                "prediction": prediction,
                "reasoning": response["content"],
                "reasoning_length": len(response["content"]),
                "tokens": response["usage"],
                "latency": response["latency"],
                "trap_type": item.get("trap", {}).get("type", "none")
            })
        except Exception as e:
            print(f"Error on item {item['id']}: {e}")
            
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-4o-mini")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    client = LLMClient(model=args.model)
    data_pattern = "code/CausalT5kBench/final_dataset/**/*.json"
    dataset = load_causal_data(data_pattern, limit=args.limit)
    
    all_results = []
    for condition in ["neutral", "skeptical", "judgmental"]:
        condition_results = run_experiment(client, dataset, condition)
        all_results.extend(condition_results)
        
    df = pd.DataFrame(all_results)
    output_path = f"results/causal/results_{args.model}.jsonl"
    df.to_json(output_path, orient="records", lines=True)
    print(f"Saved results to {output_path}")
