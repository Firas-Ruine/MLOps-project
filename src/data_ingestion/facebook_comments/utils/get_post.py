import facebook_scraper as fs

#Set the maximum number of comments to extract (true for all comments)
MAX_COMMENTS = True

def getPost(post_id):
    # get the post
    gen = fs.get_posts(
        post_urls=[post_id],
        options={"comments": MAX_COMMENTS, "progress": True}
    )
    # take 1st element of the generator which is the post we requested
    return next(gen)