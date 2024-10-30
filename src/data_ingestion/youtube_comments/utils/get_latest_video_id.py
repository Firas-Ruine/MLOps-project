
def getLatestVideoId(channel_id, youtube):
    """Get the ID of the latest video from the channel."""
    request = youtube.search().list(
        channelId=channel_id,
        order='date',
        part='id',
        maxResults=1
    )
    response = request.execute()
    if response['items']:
        return response['items'][0]['id']['videoId']
    return None