import pandas as pd
import numpy as np
import math
import os
from sklearn.metrics import cohen_kappa_score

# Loads data from an input csv file
def load_data(input_file):
    df = pd.read_csv(input_file)
    return df


def cohen_kappa():
    # Step 1: Import data from compiled annotation
    abs_path = os.path.dirname(__file__)
    rel_path = "compiled_annotations.csv"
    input_file = os.path.join(abs_path, rel_path)
    df = load_data(input_file)
    print(df)
    
    # Step 2: Isolate for overlapped data

    # Step 3: Create two arrays for the overlapped data

    # Step 4: Calculate Cohen-Kappa Score

    #define array of ratings for both raters
    rater1 = [0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    rater2 = [0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0]

    #calculate Cohen's Kappa
    print(cohen_kappa_score(rater1, rater2))

if __name__ == "__main__":
    cohen_kappa()