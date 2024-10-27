def getPostComments(post):
    comments_data = []
    # get comments
    comments = post['comments_full']
    # process comments
    for comment in comments:
        # to not include emoji comments
        if (comment['commenter_name'] != comment['comment_text']):
            comments_data.append({'text': comment['comment_text']})
    return comments_data