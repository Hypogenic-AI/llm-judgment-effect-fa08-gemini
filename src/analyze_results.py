import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_dataset(file_path, title, output_prefix):
    df = pd.read_json(file_path, lines=True)
    
    # Calculate accuracy
    df['correct'] = df['prediction'].str.lower() == df['ground_truth'].str.lower()
    
    # Group by condition
    stats = df.groupby('condition').agg({
        'correct': 'mean',
        'reasoning_length': ['mean', 'std'],
        'id': 'count'
    }).reset_index()
    stats.columns = ['condition', 'accuracy', 'reason_len_mean', 'reason_len_std', 'count']
    
    print(f"\nStats for {title}:")
    print(stats)
    
    # Visualization: Accuracy
    plt.figure(figsize=(10, 6))
    sns.barplot(x='condition', y='accuracy', data=stats, order=['neutral', 'skeptical', 'judgmental'])
    plt.title(f'Accuracy by Condition - {title}')
    plt.ylim(0, 1.1)
    plt.savefig(f'figures/{output_prefix}_accuracy.png')
    
    # Visualization: Reasoning Length
    plt.figure(figsize=(10, 6))
    sns.barplot(x='condition', y='reason_len_mean', data=stats, order=['neutral', 'skeptical', 'judgmental'])
    plt.title(f'Reasoning Depth (Chars) by Condition - {title}')
    plt.savefig(f'figures/{output_prefix}_reasoning_len.png')
    
    # Label Stability (Flip Rate)
    # We pivot to see how often labels change relative to neutral
    pivot_df = df.pivot(index='id', columns='condition', values='prediction')
    if 'neutral' in pivot_df.columns:
        if 'skeptical' in pivot_df.columns:
            pivot_df['skeptical_flip'] = pivot_df['neutral'] != pivot_df['skeptical']
        if 'judgmental' in pivot_df.columns:
            pivot_df['judgmental_flip'] = pivot_df['neutral'] != pivot_df['judgmental']
        
        flip_rates = {
            'skeptical': pivot_df['skeptical_flip'].mean() if 'skeptical_flip' in pivot_df.columns else 0,
            'judgmental': pivot_df['judgmental_flip'].mean() if 'judgmental_flip' in pivot_df.columns else 0
        }
        print(f"Flip rates relative to neutral for {title}: {flip_rates}")

if __name__ == "__main__":
    os.makedirs('figures', exist_ok=True)
    
    if os.path.exists('results/r_aio/results_gpt-4o-mini.jsonl'):
        analyze_dataset('results/r_aio/results_gpt-4o-mini.jsonl', 'r/AIO (Social)', 'r_aio')
        
    if os.path.exists('results/causal/results_gpt-4o-mini.jsonl'):
        analyze_dataset('results/causal/results_gpt-4o-mini.jsonl', 'CausalT3 (Logic)', 'causal')
