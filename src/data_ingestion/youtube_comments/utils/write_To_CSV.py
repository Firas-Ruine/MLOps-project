import pandas as pd
import os

def writeToCSV(data, result_path):
    print("Writing data to CSV file...")
    
    # Create a DataFrame with the column "text"
    df = pd.DataFrame(data, columns=["text"])  # Ensure "text" is the column name

    # Check if the file exists
    if not os.path.isfile(result_path):
        # File doesn't exist, write the header
        df.to_csv(result_path, encoding='utf-8', index=False, header=True)
    else:
        # File exists, append without writing the header
        df.to_csv(result_path, mode='a', encoding='utf-8', index=False, header=False)

    # Verify if the file exists and was written
    if os.path.exists(result_path):
        print("Data has been successfully written to the CSV file at location " + result_path)
    else:
        print("Error: The file " + result_path + " does not exist.")