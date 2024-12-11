import re

def getChannelId(channel_url):
    """Extract the channel ID from the channel URL."""
    pattern = r'https:\/\/www\.youtube\.com\/@([a-zA-Z0-9_-]+)'
    match = re.search(pattern, channel_url)
    return match.group(1) if match else None