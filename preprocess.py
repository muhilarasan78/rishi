import pandas as pd
import os

def preprocess_data(input_file="tourism_data.csv", output_file="preprocessed_tourism_data.csv"):
    """
    Loads raw tourism data and applies feature engineering.
    Combines relevant text features for content-based filtering.
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run data_generator.py first.")
        return False

    # Load the dataset
    df = pd.read_csv(input_file)

    # Fill missing values
    df = df.fillna('')

    # Feature Engineering: Combine text fields for TF-IDF
    # We combine Tags, Description, and Region to capture all relevant metadata
    df['Content'] = df['Tags'] + " " + df['Description'] + " " + df['Region']
    
    # Normalize text (optional, but good practice)
    df['Content'] = df['Content'].str.lower()

    # Save the preprocessed data
    df.to_csv(output_file, index=False)
    print(f"Data preprocessing complete. Saved to {output_file}.")
    return True

if __name__ == "__main__":
    preprocess_data()
