import pandas as pd
from utils.write_To_CSV import writeToCSV

def getCommentsClassification(input_path, result_path):
    results = []
    print("Classify the emotions of the comments:")
    df = pd.read_csv(input_path)

    # Iterate through each line in the DataFrame, skipping the header
    for line in df['text'][1:]:  # Start from the second line
        print(f"Classify the emotion for the line:\n'{line}'")
        print("1: Positive")
        print("2: Negative")
        print("3: Neutral")
        
        # Get user input and map it to emotions
        while True:
            choice = input("Enter your choice (1/2/3): ")
            if choice == '1':
                emotion = 'positive'
                break
            elif choice == '2':
                emotion = 'negative'
                break
            elif choice == '3':
                emotion = 'neutral'
                break
            else:
                print("Invalid input. Please enter 1, 2, or 3.")

        results.append({'emotion': emotion, 'text': line})

    # Save the results to a new CSV file
    writeToCSV(results, result_path)