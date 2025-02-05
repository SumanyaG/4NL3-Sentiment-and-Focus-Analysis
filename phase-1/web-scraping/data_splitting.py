import pandas as pd
import numpy as np
import math

def load_and_prepare_data(input_file):
    df = pd.read_csv(input_file)
    return df


def calculate_set_sizes(total_rows):
    base_size = math.floor(total_rows / 8)
    overlap_size = math.floor(base_size * 0.15)
    
    return base_size, overlap_size


def create_overlapping_sets(df, base_size, overlap_size):
    overlap_indices = np.random.choice(df.index, size=overlap_size, replace=False)
    overlap_data = df.loc[overlap_indices]
    
    remaining_data = df.drop(overlap_indices)
    
    datasets = [[] for _ in range(8)]
    
    splits = np.array_split(remaining_data, 7)
    
    for i in range(7):
        datasets[i] = pd.concat([splits[i], overlap_data])
    
    datasets[7] = splits[-1]
    
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
    input_file = "/Users/sg/Desktop/courses/winter-2025/4nl3/4NL3-group-project/Phase_1/Web_Scraping/interviews.csv"
    output_prefix = "interview"
    overlap_output_file = "overlap_data.csv"
    
    df = load_and_prepare_data(input_file)
    
    base_size, overlap_size = calculate_set_sizes(len(df))
    
    datasets, overlap_data = create_overlapping_sets(df, base_size, overlap_size)
    save_datasets(datasets, output_prefix)
    save_overlap_data(overlap_data, overlap_output_file)
    
    print("\nDataset Statistics:")
    print(f"Total rows in original dataset: {len(df)}")
    print(f"Base size per set: {base_size}")
    print(f"Overlap size (15%): {overlap_size}")

if __name__ == "__main__":
    main()