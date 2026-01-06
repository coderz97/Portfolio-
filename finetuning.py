# Sreya Jain Tobji
# CS-690-50 : Data Science Capstone Project
# Fall 2025

# This script generates medical notes using GPT fine-tuning approach

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import json
from openai import OpenAI, RateLimitError
import warnings
warnings.filterwarnings("ignore")


API_KEY = "your_openai_api_key_here"

TRAIN_CSV = "clean_train.csv"
TEST_CSV = "clean_test.csv"
JSONL_FILE = "fine_tune_data7.4.jsonl"
OUTPUT_TEST_CSV = "test_predictions7.4.csv"
BASE_MODEL = "gpt-3.5-turbo"
SUFFIX = "medical-notes-v7.4"        
MODEL_NAME_FILE = "fine_tuned_model7.4.txt"     

os.environ["OPENAI_API_KEY"] = API_KEY
client = OpenAI(api_key=API_KEY)




# Creating  JSONL for fine-tuning 

def create_jsonl():
    print(f"\nCreating {JSONL_FILE} from {TRAIN_CSV}...")
    df = pd.read_csv(TRAIN_CSV)

    required_cols = ["dialogue", "section_text"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing columns! Need: {required_cols}")

    #df = df.dropna(subset=required_cols).reset_index(drop=True)
    df["dialogue"] = df["dialogue"].astype(str)
    df["section_text"] = df["section_text"].astype(str)

    with open(JSONL_FILE, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            # Remove section header completely
            user_prompt = f"Conversation:\n{row['dialogue']}"

            item = {
                "messages": [
                    {"role": "user", "content": user_prompt.strip()},
                    {"role": "assistant", "content": row["section_text"].strip()}
                ]
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"JSONL created → {len(df):,} training examples saved to {JSONL_FILE}")




#  Uploading file and  Fine-tuning


def upload_file():
    print("Uploading training file...")
    file_obj = client.files.create(file=open(JSONL_FILE, "rb"), purpose="fine-tune")
    print(f"Uploaded! File ID: {file_obj.id}")
    return file_obj.id

def start_fine_tune(training_file_id):
    print("Starting fine-tuning job...")
    job = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=BASE_MODEL,
        suffix=SUFFIX,
        hyperparameters={"n_epochs": 3}
    )
    print(f"Job started: {job.id}")
    return job.id


# Status Monitoring

def wait_for_training(job_id):
    print("\nMonitoring fine-tuning job...\n")
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        status = job.status
        print(f"Status: {status}", end="")
        if job.finished_at:
            print(f" | Finished at: {time.strftime('%H:%M:%S', time.localtime(job.finished_at))}")
        else:
            print()

        if status in ["succeeded", "failed", "cancelled"]:
            print(f"\nFINAL RESULT: {status.upper()}")
            if status == "failed":
                print("Error details:", job.error)
            return job

        time.sleep(30)



# Testing the fine-tuned model


def test_model(model_name):
    if not os.path.exists(TEST_CSV):
        print(f"{TEST_CSV} not found — skipping predictions.")
        return

    print(f"\nTesting model: {model_name}")
    df = pd.read_csv(TEST_CSV)

    
    if 'dialogue' not in df.columns:
        raise ValueError("test.csv must have 'dialogue' column")

    df['dialogue'] = df['dialogue'].astype(str)

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

    def generate_safe(text, section="Unknown"):
        prompt = f"Section: {section}\n\nConversation:\n{text}"
        while True:
            try:
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=1024
                )
                return resp.choices[0].message.content.strip()
            except RateLimitError:
                print("Rate limit — sleeping 15s...")
                time.sleep(15)
            except Exception as e:
                print(f"Error: {e} — retrying in 10s...")
                time.sleep(10)

    print(f"Generating predictions for {len(df)} test cases...")
    predictions = []
    for i, row in df.iterrows():
        pred = generate_safe(row['dialogue'])  # no section argument needed
        predictions.append(pred)
        print(f"  {i+1}/{len(df)} completed")


    df["predicted_note"] = predictions
    df.to_csv(OUTPUT_TEST_CSV, index=False)
    print(f"\nALL DONE! Predictions saved to:\n→ {OUTPUT_TEST_CSV}")


# defining the full pipeline

def run_pipeline():
    print("\n" + " MEDICAL NOTE FINE-TUNING PIPELINE ".center(70, "="))

    create_jsonl()
    file_id = upload_file()
    job_id = start_fine_tune(file_id)
    job = wait_for_training(job_id)

    if job.status != "succeeded":
        print("Fine-tuning failed. Stopping.")
        return

    model_name = job.fine_tuned_model
    print(f"\nSUCCESS! Your model is ready:\n{model_name}")

    with open(MODEL_NAME_FILE, "w") as f:
        f.write(model_name)
    print(f"Model name saved to {MODEL_NAME_FILE}")

    test_model(model_name)
    print("\nPipeline completed 100% successfully!")


# running the code

if __name__ == "__main__":
    run_pipeline()