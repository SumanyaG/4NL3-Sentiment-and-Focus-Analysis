import pandas as pd
import numpy as np

file_path = "/Users/sg/Desktop/courses/winter-2025/4nl3/4NL3-group-project/phase-3/ground_truth_complete.csv" 

def generate_test_data_with_annotations(path):
    df = pd.read_csv(path, usecols = ['event','date','person','quote','True Pos','True Neg','True Team','True Individual'])
    df = df.rename(columns={df.columns[4]: 'Positive', df.columns[5]: 'Negative', df.columns[6]: 'Team', df.columns[7]: 'Individual'})

    df.to_csv("test_data_with_annotations.csv", index=False)
    return df

def generate_test_data():
    df = generate_test_data_with_annotations(file_path)
    cols_to_clear = ['Positive', 'Negative', 'Team', 'Individual']
    df[cols_to_clear] = np.nan
    df.to_csv("test_data.csv", index=False)

if __name__ == "__main__":
    generate_test_data()