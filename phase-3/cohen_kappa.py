import pandas as pd
import numpy as np
import math
import os
from sklearn.metrics import cohen_kappa_score

# Loads data from an input csv file
def load_data(input_file):
    df = pd.read_csv(input_file)
    return df

# Method for extracting duplicates from the dataset
def extract_duplicates(full_data):
    # First extract the quotes as they are mostly unique
    quotes = {}
    for idx, row in full_data.iterrows():
        quote = row['quote']
        quote = quote.replace('"', '')
        quotes[idx] = quote

    # keep track of repeated dictionary values
    # make sure that the duplications have both original and duplication
    entries = {}
    duplications = {}
    for idx,quote in quotes.items():
        if quote in entries.values():
            orig_id = [key for key, val in entries.items() if quote == val][0]
            duplications[orig_id] = quote
            duplications[idx] = quote
        else:
            entries[idx] = quote
    
    return duplications


def cohen_kappa():
    # import data from overlap and full annotations
    abs_path = os.path.dirname(__file__)
    full_file = "compiled_annotations.csv"
    df_full = load_data(os.path.join(abs_path, full_file))

    # get the duplicated quotes
    duplicates = extract_duplicates(df_full)

    # create the 2 sets of 4 ratings based on agreement
    pos_rater_1 = []
    pos_rater_2 = []
    team_rater_1 = []
    team_rater_2 = []

    # work through the keys and alternate between orig and dup
    keys = duplicates.keys()
    dup = True

    for key in keys:
        if dup:           
            # append to rater 2
            pos_rater_2.append(int(np.nan_to_num(df_full.loc[key, 'Positive?'])))
            team_rater_2.append(int(np.nan_to_num(df_full.loc[key, 'Team?'])))
            dup = False
        else:
            # append to rater 1
            pos_rater_1.append(int(np.nan_to_num(df_full.loc[key, 'Positive?'])))
            team_rater_1.append(int(np.nan_to_num(df_full.loc[key, 'Team?'])))
            dup = True

    # calculate and print the 4 Cohen-Kappa Scores
    kappa_pos_neg = cohen_kappa_score(pos_rater_1, pos_rater_2)
    kappa_team_ind = cohen_kappa_score(team_rater_1, team_rater_2)

    # Print out the scores
    print("Positive-Negative Cohen-Kappa Score: ", kappa_pos_neg)
    print("Team-Individual Cohen-Kappa Score: ", kappa_team_ind)

if __name__ == "__main__":
    cohen_kappa()