import pandas as pd
import numpy as np
import math

def load_and_prepare_data(input_file):
    df = pd.read_csv(input_file)
    return df

def calculate_set_sizes(total_rows):
    overlap_size = math.floor(total_rows * 0.15)
    base_size = math.floor((total_rows - overlap_size) / 8)
    
    return base_size, overlap_size

def create_overlapping_sets(df):
    total_instances = len(df)
    base_size, overlap_size = calculate_set_sizes(total_instances)
    
    overlap_indices = np.random.choice(df.index, size=overlap_size, replace=False)
    overlap_data = df.loc[overlap_indices]
    
    remaining_data = df.drop(overlap_indices)
    
    datasets = [[] for _ in range(8)]
    splits = np.array_split(remaining_data, 8)
    
    overlap_per_set = math.floor(overlap_size / 7)

    for i in range(7):
        if i == 6:
            start_idx = i * overlap_per_set
            overlap_subset = overlap_data.iloc[start_idx:]
        else:
            start_idx = i * overlap_per_set
            end_idx = start_idx + overlap_per_set
            overlap_subset = overlap_data.iloc[start_idx:end_idx]
            
        datasets[i] = pd.concat([splits[i], overlap_subset])

    datasets[7] = splits[7]
    
    return datasets, overlap_data

def save_datasets(datasets, output_prefix):
    for i, dataset in enumerate(datasets, 1):
        output_file = f"{output_prefix}{i}.csv"
        dataset.to_csv(output_file, index=False)
        print(f"Saved dataset {i} with {len(dataset)} rows to {output_file}")

def save_overlap_data(overlap_data, output_file):
    overlap_data.to_csv(output_file, index=False)
    print(f"Saved overlap data with {len(overlap_data)} rows to {output_file}")

def main():
    input_file = "/Users/sg/Desktop/courses/winter-2025/4nl3/4NL3-group-project/phase-1/web-scraping/interviews.csv"
    output_prefix = "interview"
    overlap_output_file = "overlap_data.csv"
    
    df = load_and_prepare_data(input_file)
    total_instances = len(df)
    base_size, overlap_size = calculate_set_sizes(total_instances)
    
    datasets, overlap_data = create_overlapping_sets(df)
    save_datasets(datasets, output_prefix)
    save_overlap_data(overlap_data, overlap_output_file)
    
    print("\nDataset Statistics:")
    print(f"Total rows in original dataset: {total_instances}")
    print(f"Base size per set: {base_size}")
    print(f"Overlap size (15%): {overlap_size}")
    print("\nSet sizes:")
    for i, dataset in enumerate(datasets, 1):
        print(f"Set {i}: {len(dataset)} instances")
        if i < 8:
            unique_instances = len(dataset.drop_duplicates())
            print(f"Set {i} unique instances: {unique_instances}")

if __name__ == "__main__":
    main()