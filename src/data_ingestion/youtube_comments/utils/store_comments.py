import pandas as pd
from utils.write_To_CSV import writeToCSV
from utils.get_channel_id import getChannelId
from utils.get_latest_video_id import getLatestVideoId
from utils.get_video_comments import getVideoComments
from googleapiclient.discovery import build

# Your YouTube Data API key
API_KEY = 'AIzaSyDTWzUmomxive8x9Q_GYmF9CTxmzDJ2qVg'

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)


def StoreComments(scraping_input_path, scraping_result_path):
    # Read channel URLs from CSV
    print('Reading channel URLs from CSV...')
    df = pd.read_csv(scraping_input_path)
    
    # Prepare a dictionary to store comments
    comments_dict = {}

        # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        video_url = row['video_url']
        print("Reading video URL ...")
        print(video_url)

        # Extract the video ID from the video URL
        video_id = video_url.split("v=")[-1].split("&")[0]
        print("Extracted video ID:")
        print(video_id)

        if video_id:
            # Fetch comments for the video
            comments = getVideoComments(video_id, youtube)
            comments_dict[video_url] = comments
        else:
            print(f"Invalid video URL: {video_url}")

    # Print or save comments
    for video_url, comments in comments_dict.items():
        print(f"Comments for {video_url}:")
        writeToCSV(comments, scraping_result_path)
