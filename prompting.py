# Sreya Jain Tobji
# CS-690-50 : Data Science Capstone Project
# Fall 2025

# This script generates medical notes using GPT prompting approach.

import os
import pandas as pd
import time
from openai import OpenAI


API_KEY = "your_openai_api_key_here"

os.environ["OPENAI_API_KEY"] = API_KEY
client = OpenAI(api_key=API_KEY)

TEST_CSV = "clean_test.csv"
OUTPUT_TEST_CSV = "test_predictions_prompting.csv"
MODEL_NAME = "gpt-4"  # or "gpt-3.5-turbo"

# Load test data
df = pd.read_csv(TEST_CSV)
if 'dialogue' not in df.columns:
    raise ValueError("Test CSV must have a 'dialogue' column")

df['dialogue'] = df['dialogue'].astype(str)

# Detailed system prompt including instructions for each heading
system_prompt = """
You are an expert medical scribe. Convert doctor-patient conversations into professional SOAP/Epic notes. 
Use these section headings **in order**. Only include sections that have relevant information, and never invent facts.

Chief Complaint (CC): One-line summary of patient's main reason for encounter.  
History of Present Illness (HPI): Narrative description including onset, duration, severity, location, quality, associated symptoms, aggravating/relieving factors, prior treatments.  
Review of Systems (ROS): Pertinent positives and negatives from different organ systems.  
Past Medical History (PMH): Chronic conditions, past hospitalizations, surgeries.  
Medications (Meds): Current medications with dose/frequency if known.  
Allergies: Drug, food, or environmental allergies with reactions if known.  
Social History (SH): Lifestyle, habits, occupation, living situation.  
Physical Exam (PE): Vital signs and relevant objective findings by system.  
Assessment: Clinician’s interpretation or list of problems/diagnoses.  
Plan: Management strategy for each problem, including medications, labs, procedures, patient education, follow-up.

Output in clear sections with headings exactly as above.
"""

# Function to safely generate model response
def generate_safe(text):
    prompt = f"Conversation:\n{text}"
    while True:
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1024
            )
            return resp.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error: {e} — retrying in 10s...")
            time.sleep(10)

# Generate SOAP notes for all test examples
predictions = []
for i, row in df.iterrows():
    pred = generate_safe(row['dialogue'])
    predictions.append(pred)
    print(f"{i+1}/{len(df)} done")

df["predicted_note"] = predictions
df.to_csv(OUTPUT_TEST_CSV, index=False)
print(f"\nALL DONE! Predictions saved to {OUTPUT_TEST_CSV}")
