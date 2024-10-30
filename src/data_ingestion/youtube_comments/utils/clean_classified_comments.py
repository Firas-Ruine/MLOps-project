import pandas as pd
import neattext.functions as nfx

def cleanClassifiedComments(input_path, cleaned_output_path):
    print("Cleaning classified comments...")
    
    # Read the classified comments from the CSV
    df = pd.read_csv(input_path)
    
    # Check if 'text' column exists
    if 'text' not in df.columns:
        print("Error: 'text' column not found in classified comments.")
        return

    # Clean comments using neattext
    df['cleaned_text'] = df['text'].apply(nfx.remove_special_characters)
    df['cleaned_text'] = df['cleaned_text'].apply(nfx.remove_userhandles)
    df['cleaned_text'] = df['cleaned_text'].apply(nfx.remove_stopwords)
    df['cleaned_text'] = df['cleaned_text'].apply(nfx.remove_emojis)
    

    # Save the cleaned comments to a new CSV file
    df.to_csv(cleaned_output_path, index=False)
    print("Cleaned comments have been saved to " + cleaned_output_path)