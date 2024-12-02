import pandas as pd
from utils.write_To_CSV import writeToCSV

def getCommentsClassification(input_path, result_path):
    results = []
    print("Classify the emotions of the comments:")
    df = pd.read_csv(input_path)
    for line in df['text'][1:]:  # Start from the second line
        results.append({'text': line})
    writeToCSV(results, result_path)