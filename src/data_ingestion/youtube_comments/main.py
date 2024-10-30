from utils.store_comments import StoreComments
import utils.youtube_comments_classification as ycc
import os
from utils.clean_classified_comments import cleanClassifiedComments

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SCRAPING_INPUT = os.path.join(BASE_PATH, 'inputs', 'channels.csv')
SCRAPING_RESULT = os.path.join(BASE_PATH, 'results', 'youtube_comments.csv')
CLASSIFICATION_RESULT = os.path.join(BASE_PATH, 'results', 'youtube_comments_classified.csv')
CLEANING_RESULT = os.path.join(BASE_PATH, 'results', 'youtube_comments_cleaned.csv')

def main():
    StoreComments(SCRAPING_INPUT, SCRAPING_RESULT)
    if os.path.exists(CLASSIFICATION_RESULT):
        if input("Do you want to proceed with the classification of the comments? (y/n): ") == 'y':
            ycc.main(SCRAPING_RESULT, CLASSIFICATION_RESULT)
        else:
            print("Classification of comments aborted.")
    else:
        ycc.main(SCRAPING_RESULT, CLASSIFICATION_RESULT)
    cleanClassifiedComments(CLASSIFICATION_RESULT, CLEANING_RESULT)
    
if __name__ == '__main__':
    main()
