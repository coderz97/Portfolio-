# Sreya Jain Tobji
# CS-690-50 : Data Science Capstone Project
# Fall 2025

# This script intends to find and drop rows containing conversational content that is flagged as unsafe or inappropriate using the OpenAI Moderation API.

import pandas as pd
from openai import OpenAI
import os


API_KEY = "your_openai_api_key_here"
os.environ["OPENAI_API_KEY"] = API_KEY
client = OpenAI(api_key=API_KEY)

TRAIN_CSV = "data/training_data.csv"
TEST_CSV = "data/test.csv"
CLEAN_TRAIN_CSV = "clean_train.csv"
CLEAN_TEST_CSV = "clean_test.csv"

def moderate(text):
    """
    Returns True if text is flagged as unsafe, False otherwise
    """
    try:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=text
        )
        return response.results[0].flagged
    except Exception as e:
        print(f"Moderation API error: {e}")
        return True  # treat errors as flagged for safety

def is_row_flagged(row, columns):
    """
    Returns True if any column in the row is flagged by moderation.
    Splits text into sentences and checks each sentence individually for stricter filtering.
    """
    import re
    for col in columns:
        text = str(row[col])
        # Split into sentences for stricter check
        sentences = re.split(r'[.!?]\s+', text)
        for sentence in sentences:
            if moderate(sentence):
                return True
    return False

# ---- Clean TRAINING DATA ----
train_df = pd.read_csv(TRAIN_CSV)
required_cols_train = ["dialogue", "section_text"]

flagged_train_rows = []
for i, row in train_df.iterrows():
    if is_row_flagged(row, required_cols_train):
        flagged_train_rows.append(i)

print(f"Flagged training rows: {len(flagged_train_rows)} / {len(train_df)}")
clean_train_df = train_df.drop(flagged_train_rows).reset_index(drop=True)
clean_train_df.to_csv(CLEAN_TRAIN_CSV, index=False)
print(f"Clean training data saved: {CLEAN_TRAIN_CSV}")

# ---- Clean TEST DATA ----
test_df = pd.read_csv(TEST_CSV)
if 'dialogue' not in test_df.columns:
    raise ValueError("Test CSV must have a 'dialogue' column")

flagged_test_rows = []
for i, row in test_df.iterrows():
    if is_row_flagged(row, ['dialogue']):
        flagged_test_rows.append(i)

print(f"Flagged test rows: {len(flagged_test_rows)} / {len(test_df)}")
clean_test_df = test_df.drop(flagged_test_rows).reset_index(drop=True)
clean_test_df.to_csv(CLEAN_TEST_CSV, index=False)
print(f"Clean test data saved: {CLEAN_TEST_CSV}")
