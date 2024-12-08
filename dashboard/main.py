from flask import Flask, request, render_template
from googleapiclient.discovery import build
import joblib
from flask import current_app as app
# Initialize Flask app
app = Flask(__name__)
MODEL_PATH = '../text_sentiment_model.pkl'
model = joblib.load(MODEL_PATH)
API_KEY = 'AIzaSyDTWzUmomxive8x9Q_GYmF9CTxmzDJ2qVg'

youtube = build('youtube', 'v3', developerKey=API_KEY)

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        youtube_url = request.form.get("youtube_url")
        if not youtube_url:
            return "YouTube URL is required", 400

        comments = []
        video_id = youtube_url.split("v=")[-1].split("&")[0]
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=10
        )
        response = request.execute()

        while response:
            for item in response['items']:
                comment = {'text': item['snippet']['topLevelComment']['snippet']['textDisplay']}
                comments.append(comment)

            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=response['nextPageToken'],
                    maxResults=10
                )
                response = request.execute()
            else:
                break

        predictions = model.predict([comment['text'] for comment in comments])
        for i, comment in enumerate(comments):
            comment['sentiment'] = predictions[i]

        return render_template("home/youtube.html", comments=comments)
    else :
        return render_template('home/youtube.html')


if __name__ == '__main__':
    app.run(debug=True)
