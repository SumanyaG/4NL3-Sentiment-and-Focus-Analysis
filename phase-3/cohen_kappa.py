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
    # import data from overlap and full annotations
    abs_path = os.path.dirname(__file__)
    full_file = "compiled_annotations.csv"
    overlap_file = "overlap_data.csv"
    df_full = load_data(os.path.join(abs_path, full_file))
    df_overlap = load_data(os.path.join(abs_path, overlap_file))

    overlap = df_full.loc[(df_full['event'].isin(df_overlap['event'])) & 
                          (df_full['date'].isin(df_overlap['date'])) & 
                          (df_full['person'].isin(df_overlap['person'])) & 
                          (df_full['quote'].isin(df_overlap['quote']))]
    print(overlap)

    #for index,row in df_full.iterrows():
    #    
    #    print(row['person'], row['quote'])
    
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