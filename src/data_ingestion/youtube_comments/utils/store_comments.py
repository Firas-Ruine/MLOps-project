import pandas as pd
from utils.write_To_CSV import writeToCSV
from utils.get_channel_id import getChannelId
from utils.get_latest_video_id import getLatestVideoId
from utils.get_video_comments import getVideoComments
from googleapiclient.discovery import build

# Your YouTube Data API key
API_KEY = ''

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)


def StoreComments(scraping_input_path, scraping_result_path):
    # Read channel URLs from CSV
    print('Reading channel URLs from CSV...')
    df = pd.read_csv(scraping_input_path)
    
    # Prepare a dictionary to store comments
    comments_dict = {}

    for index, row in df.iterrows():
        channel_url = row['channel_url']
        channel_id = getChannelId(channel_url)
        
        if channel_id:
            video_id = getLatestVideoId(channel_id, youtube)
            if video_id:
                comments = getVideoComments(video_id, youtube)
                comments_dict[channel_url] = comments
            else:
                print(f"No videos found for channel: {channel_url}")
        else:
            print(f"Invalid channel URL: {channel_url}")

    # Print or save comments
    for channel_url, comments in comments_dict.items():
        print(f"Comments for {channel_url}:")
        writeToCSV(comments, scraping_result_path)
