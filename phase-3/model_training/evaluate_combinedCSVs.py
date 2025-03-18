import pandas as pd
import numpy as np
# from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score
from collections import Counter
import json
import os

current_dir = os.path.dirname(__file__)

# Step 1: Load and preprocess the data
def load_and_preprocess_data(train_file_path, test_file_path):
    # Load the training and testing CSV files
    train_data = pd.read_csv(train_file_path)
    test_data = pd.read_csv(test_file_path)

    # Standardize column names by removing trailing '?' if present
    train_data.columns = train_data.columns.str.rstrip('?')
    test_data.columns = test_data.columns.str.rstrip('?')

    # Verify required columns exist
    required_columns = ["Positive", "Negative", "Team", "Individual", "quote"]
    for column in required_columns:
        if column not in train_data.columns:
            raise KeyError(f"Column '{column}' not found in training data.")
        if column not in test_data.columns:
            raise KeyError(f"Column '{column}' not found in testing data.")

    # Extract the text and labels from training data
    X_train = train_data["quote"].tolist()
    y_train_sentiment = np.nan_to_num(train_data[["Positive", "Negative"]].values, nan=0).astype(int)  # Replace NaN with 0
    y_train_focus = np.nan_to_num(train_data[["Team", "Individual"]].values, nan=0).astype(int)  # Replace NaN with 0

    # Extract the text and labels from testing data
    X_test = test_data["quote"].tolist()
    y_test_sentiment = np.nan_to_num(test_data[["Positive", "Negative"]].values, nan=0).astype(int)  # Replace NaN with 0
    y_test_focus = np.nan_to_num(test_data[["Team", "Individual"]].values, nan=0).astype(int)  # Replace NaN with 0

    # Vectorize the text data
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    return X_train_vec, X_test_vec, y_train_sentiment, y_test_sentiment, y_train_focus, y_test_focus


# Step 2: Train and evaluate models
def train_and_evaluate_models(X_train_vec, X_test_vec, y_train, y_test, task_name):
    # Feedforward Neural Network
    nn_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
    nn_model.fit(X_train_vec, y_train)
    y_pred_nn = nn_model.predict(X_test_vec)
    return y_pred_nn


# Step 3: Baselines
def majority_baseline(y_true):
    majority_label = Counter(y_true).most_common(1)[0][0]
    return [majority_label] * len(y_true)


def evaluate_baselines(y_train, y_test, task_name):
    # Majority Baseline
    majority_label = Counter(y_train).most_common(1)[0][0]  # Use training set to determine majority class
    y_test_majority = [majority_label] * len(y_test)  # Predict majority class for all test instances
    majority_accuracy = accuracy_score(y_test, y_test_majority)
    majority_f1 = f1_score(y_test, y_test_majority, average="weighted")

    return majority_accuracy, majority_f1


# Step 4: Save results
def save_results(results, file_path):
    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)


# Step 5: Save predictions to CSV
def save_predictions_to_csv(y_pred_sentiment, y_pred_focus, file_path):
    # Create a DataFrame with the predictions
    predictions_df = pd.DataFrame({
        "Positive?": ["" if pred == 0 else "1" for pred in y_pred_sentiment],
        "Negative?": ["" if pred == 1 else "1" for pred in y_pred_sentiment],
        "Team?": ["" if pred == 0 else "1" for pred in y_pred_focus],
        "Individual?": ["" if pred == 1 else "1" for pred in y_pred_focus]
    })

    # Save the DataFrame to a CSV file
    predictions_df.to_csv(file_path, index=False)


# Main function
def main():
    # Construct the file paths relative to the current file
    train_file_path = os.path.join(current_dir, "../training_data.csv")
    test_file_path = os.path.join(current_dir, "../test_data_with_annotations.csv")
    train_file_path = os.path.normpath(train_file_path)
    test_file_path = os.path.normpath(test_file_path)

    # Load and preprocess the data
    try:
        X_train_vec, X_test_vec, y_train_sentiment, y_test_sentiment, y_train_focus, y_test_focus = load_and_preprocess_data(train_file_path, test_file_path)
    except KeyError as e:
        print(f"Error: {e}")
        return

    # Train and evaluate models for sentiment (Positive vs. Negative)
    y_pred_sentiment = train_and_evaluate_models(X_train_vec, X_test_vec, y_train_sentiment[:, 0], y_test_sentiment[:, 0], "sentiment")

    # Train and evaluate models for focus (Team vs. Individual)
    y_pred_focus = train_and_evaluate_models(X_train_vec, X_test_vec, y_train_focus[:, 0], y_test_focus[:, 0], "focus")

    # Evaluate baselines (optional, since the results are not being used)
    evaluate_baselines(y_train_sentiment[:, 0], y_test_sentiment[:, 0], "sentiment")  # Pass y_train and y_test
    evaluate_baselines(y_train_focus[:, 0], y_test_focus[:, 0], "focus")  # Pass y_train and y_test

    # Save predictions to CSV
    save_predictions_to_csv(y_pred_sentiment, y_pred_focus, os.path.join(current_dir, "../sample_outputs/annotation_results.csv"))
    print("Predictions saved to sample_outputs/annotation_results.csv")

if __name__ == "__main__":
    main()