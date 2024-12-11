import pandas as pd
import hashlib
import joblib 




def classify_data(input_file, output_file, model_file):

    df = pd.read_csv(input_file)


    def sanitize_text(text):
        if isinstance(text, str): 
            return text.replace('\n', ' ').replace('\r', ' ').strip()
        return text

    df['text'] = df['text'].apply(sanitize_text)

    def generate_text_id(text):
        return hashlib.md5(text.encode()).hexdigest()[:10]

    df['textID'] = df['text'].apply(generate_text_id)
    df['selected_text'] = df['text']


    model = joblib.load(model_file)

    def classify_text(text):
        prediction = model.predict([text])  
        return prediction[0] 

    df['sentiment'] = df['text'].apply(classify_text)

    df.to_csv(output_file, index=False, columns=['textID', 'text', 'selected_text' ,'sentiment'])
    print(f"Classified data saved to {output_file}")
