import joblib
import os
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score


base_path = os.path.dirname(os.path.abspath(__file__))

# Load dataset and select only 'text' and 'sentiment' columns
test_df = pd.read_csv(os.path.join(base_path, '../dataset', 'test.csv'), encoding='cp1252')
# Load the saved model
test_df = test_df[test_df['text'].notna()]  # Drop rows where 'text' is NaN
test_df['text'] = test_df['text'].astype(str)  # Convert all 'text' values to strings

# Log any non-string entries and remove them
non_string_entries = test_df[test_df['text'].apply(lambda x: not isinstance(x, str))]
if not non_string_entries.empty:
    print("Warning: The following rows have non-string 'text' entries and will be removed:\n", non_string_entries)
    test_df = test_df[test_df['text'].apply(lambda x: isinstance(x, str))]

# Load the saved model
model = joblib.load('src/models/text_sentiment_model.pkl')

# Make predictions on the cleaned test set
y_pred = model.predict(test_df['text'])

# Evaluate the model
print("Model Evaluation Metrics:")
print("\nAccuracy:", accuracy_score(test_df['sentiment'], y_pred))
print("\nClassification Report:\n", classification_report(test_df['sentiment'], y_pred))