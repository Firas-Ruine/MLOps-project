import os
import utils.facebook_comments_scraping as fcs
import utils.facebook_comments_classification as fcc

SCRAPING_INPUT = 'C:\PFE\mlops\MLOps-project\src\data_ingestion\\facebook_comments\inputs\posts_ids.csv'
SCRAPING_RESULT = 'C:\PFE\mlops\MLOps-project\src\data_ingestion\\facebook_comments\\results\\facebook_comments.csv'
CLASSIFICATION_RESULT = 'C:\PFE\mlops\MLOps-project\src\data_ingestion\\facebook_comments\\results\\facebook_comments_classified.csv'

def main():
    # SCRAPING
    if os.path.exists(SCRAPING_RESULT):
        if input("The file "+ SCRAPING_RESULT +"already exists. Do you want to add to it? (y/n): ") == 'y':
            fcs.main(SCRAPING_INPUT, SCRAPING_RESULT)
        else:
            print("Skipped scraping of comments.")
    else: 
        fcs.main(SCRAPING_INPUT, SCRAPING_RESULT)
        
    # CLASSIFICATION
    if os.path.exists(CLASSIFICATION_RESULT):
        if input("Do you want to proceed with the classification of the comments? (y/n): ") == 'y':
            fcc.main(SCRAPING_RESULT, CLASSIFICATION_RESULT)
        else:
            print("Classification of comments aborted.")
    else:
        fcc.main(SCRAPING_RESULT, CLASSIFICATION_RESULT)

if __name__ == '__main__':
    main()