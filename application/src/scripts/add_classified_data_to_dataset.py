import pandas as pd


def add_classified_data_to_dataset(train_file, new_data_file):
    train_df = pd.read_csv(train_file)

    new_data_df = pd.read_csv(new_data_file)

    missing_columns = [col for col in train_df.columns if col not in new_data_df.columns]
    for col in missing_columns:
        new_data_df[col] = None  

    new_data_df = new_data_df[train_df.columns]

    updated_train_df = pd.concat([train_df, new_data_df], ignore_index=True)

    updated_train_df = updated_train_df.drop_duplicates(subset='textID', keep='first')

    updated_train_df.to_csv(train_file, index=False)

    print(f"Train dataset has been updated and saved to {train_file}")
