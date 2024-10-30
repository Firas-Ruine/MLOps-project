def getVideoComments(video_id, youtube):
    """Get comments from the video."""
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=10
    )
    response = request.execute()
    
    while response:
        for item in response['items']:
            comment = {'text':item['snippet']['topLevelComment']['snippet']['textDisplay']}
            comments.append(comment)

        # Check if there are more comments
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

    return comments