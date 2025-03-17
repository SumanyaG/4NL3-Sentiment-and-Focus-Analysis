import pandas as pd
import numpy as np
import math
import os

def extract_duplicates():
    # import data from overlap and full annotations
    abs_path = os.path.dirname(__file__)
    full_file = "compiled_annotations.csv"
    df_full = pd.read_csv(os.path.join(abs_path, full_file))

    # First extract the quotes as they are mostly unique
    quotes = {}
    for idx, row in df_full.iterrows():
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
    
    # using the keys, add all the duplicate data to a list and convert to a dataframe
    keys = duplications.keys()
    dups = []

    for key in keys:
        dups.append(df_full.loc[key])

    dup_data = pd.DataFrame(dups)

    # print to a csv
    dup_data.to_csv("duplicate_data.csv", sep=",")

if __name__ == "__main__":
    extract_duplicates()