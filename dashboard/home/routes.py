# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from dashboard.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from googleapiclient.discovery import build
import joblib
import csv
# Load the sentiment analysis model
MODEL_PATH = 'emotion_classifier_pipe_lr.pkl'
model = joblib.load(MODEL_PATH)

# YouTube API setup
API_KEY = 'AIzaSyDTWzUmomxive8x9Q_GYmF9CTxmzDJ2qVg'
youtube = build('youtube', 'v3', developerKey=API_KEY)


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/youtube', methods=['GET', 'POST'])
@login_required
def youtube_route():
    comments = []  # Initialize comments list
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')
        if youtube_url:
            try:
                with open('src/data_ingestion/youtube_comments/inputs/channels.csv', 'a', newline='\n', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([])
                    writer.writerow([youtube_url])
                # Parse video ID from URL (simplified for demonstration)
                video_id = youtube_url.split("v=")[-1]
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
            flash("Please enter a valid YouTube URL.", "danger")

    return render_template('home/youtube.html', segment='youtube', comments=comments)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        return segment if segment else 'index'
    except Exception:
        return None
