from flask import Flask, render_template, request, flash
from googleapiclient.discovery import build
import joblib
import csv
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

MODEL_PATH = 'src/models/emotion_classifier_pipe_lr.pkl'
model = joblib.load(MODEL_PATH)

API_KEY = 'AIzaSyDTWzUmomxive8x9Q_GYmF9CTxmzDJ2qVg'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    Handles various YouTube URL formats.
    """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/facebook')
def facebook_route():
    return render_template('facebook.html')

@app.route('/youtube', methods=['GET', 'POST'])
def youtube_route():
    comments = []  # Initialize comments list
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')
        if youtube_url:
            video_id = extract_video_id(youtube_url)
            if video_id:
                try:
                    # Log the URL into the CSV file
                    with open('src/data_ingestion/youtube_comments/inputs/channels.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([youtube_url])

                    # Fetch comments using YouTube API
                    response = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=100
                    ).execute()

                    for item in response.get('items', []):
                        comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                        # Predict sentiment
                        sentiment = model.predict([comment_text])[0]
                        comments.append({
                            'text': comment_text,
                            'sentiment': sentiment
                        })

                        # Count sentiment
                        if sentiment == "positive":
                            positive_count += 1
                        elif sentiment == "negative":
                            negative_count += 1
                        else:
                            neutral_count += 1

                    # Flash message with sentiment counts
                    flash(f"Comments fetched successfully! Positive: {positive_count}, Negative: {negative_count}, Neutral: {neutral_count}", "success")

                except Exception as e:
                    flash(f"Error fetching comments: {str(e)}", "danger")
            else:
                flash("Invalid YouTube URL. Please check and try again.", "danger")
        else:
            flash("Please enter a valid YouTube URL.", "danger")

    sentiment_data = {
        'positive': positive_count,
        'negative': negative_count,
        'neutral': neutral_count
    }
    return render_template('youtube.html', comments=comments, sentiment_data=sentiment_data)

if __name__ == "__main__":
    app.run(debug=True)
