import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import os
import joblib

base_path = os.path.dirname(os.path.abspath(__file__))

# Load dataset and select only 'text' and 'sentiment' columns
df = pd.read_csv(os.path.join(base_path, '../../data', 'train.csv'), encoding='utf-8')

# Handle missing values in the 'text' column by filling them with empty strings
df['text'] = df['text'].fillna("")
df = df[df['text'].notna()]  # Drop rows where 'text' is NaN
df['text'] = df['text'].astype(str)  # Convert all 'text' values to strings

# Log any non-string entries and remove them
non_string_entries = df[df['text'].apply(lambda x: not isinstance(x, str))]
if not non_string_entries.empty:
    print("Warning: The following rows have non-string 'text' entries and will be removed:\n", non_string_entries)
    df = df[df['text'].apply(lambda x: isinstance(x, str))]
# Create a pipeline for text processing and model training
pipeline = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression()
)

# Train the model on the training data
pipeline.fit(df['text'], df['sentiment'])

# Save the model
joblib.dump(pipeline, 'src/models/emotion_classifier_pipe_lr.pkl')

print("Model saved in 'emotion_classifier_pipe_lr.pkl'")