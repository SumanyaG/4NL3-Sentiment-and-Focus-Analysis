import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score
from collections import Counter
import json
import os

# Step 1: Load and preprocess the data
def load_and_preprocess_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract the text and labels
    texts = data["quote"].tolist()

    # Convert labels to binary values (1 for "Yes", 0 for "No" or blank)
    labels_sentiment = data[["Positive?", "Negative?"]].fillna(0).astype(int).values
    labels_focus = data[["Team?", "Individual?"]].fillna(0).astype(int).values

    # Split the data into training and testing sets
    X_train, X_test, y_train_sentiment, y_test_sentiment, y_train_focus, y_test_focus = train_test_split(
        texts, labels_sentiment, labels_focus, test_size=0.2, random_state=42
    )

    # Vectorize the text data
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    return X_train_vec, X_test_vec, y_train_sentiment, y_test_sentiment, y_train_focus, y_test_focus


# Step 2: Train and evaluate models
def train_and_evaluate_models(X_train_vec, X_test_vec, y_train, y_test, task_name):
    results = {}

    # Logistic Regression
    lr_model = LogisticRegression()
    lr_model.fit(X_train_vec, y_train)
    y_pred_lr = lr_model.predict(X_test_vec)
    results["Logistic_Regression"] = {
        "accuracy": accuracy_score(y_test, y_pred_lr),
        "f1_score": f1_score(y_test, y_pred_lr, average="weighted")
    }

    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_vec, y_train)
    y_pred_rf = rf_model.predict(X_test_vec)
    results["Random_Forest"] = {
        "accuracy": accuracy_score(y_test, y_pred_rf),
        "f1_score": f1_score(y_test, y_pred_rf, average="weighted")
    }

    # Feedforward Neural Network
    nn_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
    nn_model.fit(X_train_vec, y_train)
    y_pred_nn = nn_model.predict(X_test_vec)
    results["Neural_Network"] = {
        "accuracy": accuracy_score(y_test, y_pred_nn),
        "f1_score": f1_score(y_test, y_pred_nn, average="weighted")
    }

    return results


# Step 3: Baselines
def random_baseline(y_true):
    unique_labels = np.unique(y_true)
    return np.random.choice(unique_labels, size=len(y_true))


def majority_baseline(y_true):
    majority_label = Counter(y_true).most_common(1)[0][0]
    return [majority_label] * len(y_true)


def evaluate_baselines(y_test, task_name):
    # Random Baseline
    y_test_random = random_baseline(y_test)
    random_accuracy = accuracy_score(y_test, y_test_random)

    # Majority Baseline
    y_test_majority = majority_baseline(y_test)
    majority_accuracy = accuracy_score(y_test, y_test_majority)

    return {
        f"random_baseline_accuracy_{task_name}": random_accuracy,
        f"majority_baseline_accuracy_{task_name}": majority_accuracy
    }


# Step 4: Save results
def save_results(results, file_path):
    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)


# Main function
def main():
    # Construct the file path relative to the current file
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "../annotations/interview1_annotations (1).csv")
    file_path = os.path.normpath(file_path)

    # Load and preprocess the data
    X_train_vec, X_test_vec, y_train_sentiment, y_test_sentiment, y_train_focus, y_test_focus = load_and_preprocess_data(file_path)

    # Train and evaluate models for sentiment (Positive vs. Negative)
    sentiment_results = train_and_evaluate_models(X_train_vec, X_test_vec, y_train_sentiment[:, 0], y_test_sentiment[:, 0], "sentiment")

    # Train and evaluate models for focus (Team vs. Individual)
    focus_results = train_and_evaluate_models(X_train_vec, X_test_vec, y_train_focus[:, 0], y_test_focus[:, 0], "focus")

    # Evaluate baselines
    sentiment_baselines = evaluate_baselines(y_test_sentiment[:, 0], "sentiment")
    focus_baselines = evaluate_baselines(y_test_focus[:, 0], "focus")

    # Combine all results
    results = {
        "sentiment": sentiment_results,
        "focus": focus_results,
        "baselines": {**sentiment_baselines, **focus_baselines}
    }

    # Save results
    save_results(results, "results.json")
    print("Results saved to results.json")


if __name__ == "__main__":
    main()