#!/usr/bin/env python
# coding: utf-8

"""
Emotion Detection in Text
A pipeline to train and evaluate a Logistic Regression model for emotion detection,
with metrics and artifacts logged to an external MLflow server.
"""

# Imports
import os
import pandas as pd
import numpy as np
import neattext.functions as nfx
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, ConfusionMatrixDisplay
import joblib
import mlflow
import mlflow.sklearn

# Set MLflow Tracking URI and Experiment
MLFLOW_TRACKING_URI = "http://172.26.0.1:5003" 
MLFLOW_EXPERIMENT_NAME = "emotion_detection_experiment"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

# Load Dataset
DATA_PATH = os.path.join(os.getcwd(), "data", "train.csv")
df = pd.read_csv(DATA_PATH, encoding="utf-8")

# Data Exploration and Visualization
sns.countplot(x="sentiment", data=df)
plt.savefig("sentiment_distribution.png")
mlflow.log_artifact("sentiment_distribution.png")

# Clean Dataset
df["text"] = df["text"].fillna("").astype(str)  # Handle missing values
df["Clean_Text"] = df["text"].apply(nfx.remove_userhandles).apply(nfx.remove_stopwords)

# Features and Labels
Xfeatures = df["Clean_Text"]
ylabels = df["sentiment"]

# Split Data
x_train, x_test, y_train, y_test = train_test_split(Xfeatures, ylabels, test_size=0.3, random_state=42)

# Build Pipeline
pipe_lr = Pipeline(steps=[("cv", CountVectorizer()), ("lr", LogisticRegression(max_iter=100, solver="lbfgs"))])

# End any active run before starting a new one
if mlflow.active_run():
    print(f"Ending active run: {mlflow.active_run().info.run_id}")
    mlflow.end_run()

# Start an MLflow Run
with mlflow.start_run():
    # Train the Model
    pipe_lr.fit(x_train, y_train)

    # Log Model Parameters
    mlflow.log_param("model_type", "Logistic Regression")
    mlflow.log_param("vectorizer", "CountVectorizer")
    mlflow.log_param("train_test_split", "70:30")
    mlflow.log_param("vocab_size", len(pipe_lr["cv"].vocabulary_))
    mlflow.log_param("max_iter", pipe_lr["lr"].max_iter)
    mlflow.log_param("solver", pipe_lr["lr"].solver)

    # Evaluate the Model
    predictions = pipe_lr.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average="weighted")
    recall = recall_score(y_test, predictions, average="weighted")
    f1 = f1_score(y_test, predictions, average="weighted")

    # Log Metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    # Log Confusion Matrix
    cm_display = ConfusionMatrixDisplay.from_estimator(pipe_lr, x_test, y_test)
    cm_display.figure_.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")

    # Log Cleaned Dataset
    df.to_csv("cleaned_dataset.csv", index=False)
    mlflow.log_artifact("cleaned_dataset.csv")

    # Log Model
    mlflow.sklearn.log_model(pipe_lr, artifact_path="emotion_classifier_pipe_lr")

    # Save Model Locally and Log as an Artifact
    model_filepath = "models/emotion_classifier_pipe_lr.pkl"
    os.makedirs(os.path.dirname(model_filepath), exist_ok=True)
    joblib.dump(pipe_lr, model_filepath)
    mlflow.log_artifact(model_filepath)

    print(f"Logged model with accuracy: {accuracy:.2f}")

# Test Prediction
test_text = "This book was so interesting it made me happy"
test_prediction = pipe_lr.predict([test_text])
print(f"Prediction for '{test_text}': {test_prediction[0]}")

# Log Prediction Probability
proba = pipe_lr.predict_proba([test_text])
mlflow.log_metric("avg_prediction_confidence", np.max(proba))

# Save Model Pipeline Locally
pipeline_path = "../../src/models/emotion_classifier_pipe_lr.pkl"
os.makedirs(os.path.dirname(pipeline_path), exist_ok=True)
with open(pipeline_path, "wb") as pipeline_file:
    joblib.dump(pipe_lr, pipeline_file)

print("Pipeline saved successfully.")
