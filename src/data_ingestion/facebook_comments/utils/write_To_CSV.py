import pandas as pd
import os

def writeToCSV(data, result_path):
    print("Writing data to CSV file...")
    df = pd.DataFrame(data)
    # if file does not exist write header
    if not os.path.isfile(result_path):
        df.to_csv(result_path, encoding='utf-8', index=False)
    else:  # else it exists so append without writing the header
        df.to_csv(result_path, mode='a', encoding='utf-8', index=False, header=False)
        
    if os.path.exists(result_path):
        print("Data have been successfully written to the CSV file at location " + result_path)
    else:
        print("Error: The file "+result_path+" does not exist.")