from classify_data import classify_data
from add_classified_data_to_dataset import add_classified_data_to_dataset

input_file = 'src/data_ingestion/youtube_comments/results/youtube_comments_classified.csv'
output_file = 'src/scripts/classified_comments.csv'
model_file = 'src/models/emotion_classifier_pipe_lr.pkl'
train_file = 'data/train.csv' 


classify_data(input_file , output_file , model_file)
add_classified_data_to_dataset(train_file , output_file)

