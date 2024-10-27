from utils.get_post_comments import getPostComments
from utils.get_post import getPost
from utils.read_posts_ids_from_CSV import readPostsIdsFromCSVFile
from utils.write_To_CSV import writeToCSV

def getPostsComments(input_path, result):
    print("Getting posts comments...")
    data = []
    posts_ids = readPostsIdsFromCSVFile(input_path)
    for post_id in posts_ids:
        post = getPost(post_id)
        comments_data = getPostComments(post)
        data.extend(comments_data)
    writeToCSV(data, result)
