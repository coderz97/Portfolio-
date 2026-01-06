# Sreya Jain Tobji
# CS-690-50 : Data Science Capstone Project
# Fall 2025

# This script creates the test and training datasets by randomly selecting records from the MTS augmented dataset

import pandas as pd

#Combining the augmented datsets into one CSV file

file1 = "data/MTS-Dialog-Augmented-TrainingSet-1-En-FR-EN-2402-Pairs .csv"
file2 = "data/MTS-Dialog-Augmented-TrainingSet-2-EN-ES-EN-2402-Pairs.csv"
file3 = "data/MTS-Dialog-Augmented-TrainingSet-3-FR-and-ES-3603-Pairs-final.csv"


combined = pd.concat([pd.read_csv(file1),
                      pd.read_csv(file2),
                      pd.read_csv(file3)], ignore_index=True)

combined.to_csv("data/MTS-augmented_data.csv", index=False)


#picking 100 records at random from the main dataset (80%) and augmented dataset (20%)

df_main = pd.read_csv("data/MTS-Dialog-TrainingSet.csv")
df_aug = pd.read_csv("data/MTS-augmented_data.csv")

# Number of records to pick
n_total = 100
n_main = int(n_total * 0.8)  # 80% main
n_aug = n_total - n_main     # 20% augmented

# Randomly picking records from each dataset
df_main_sample = df_main.sample(n=n_main, random_state=42)
df_aug_sample = df_aug.sample(n=n_aug, random_state=42)

# Combine and shuffle the final dataset
final_df = pd.concat([df_main_sample, df_aug_sample], ignore_index=True)
final_df = final_df.sample(frac=1, random_state=42)  


final_df.to_csv("data/training_data.csv", index=False)

#test data
df_all = pd.concat([df_main, df_aug], ignore_index=True)

# Remove training rows to avoid repetition
df_unused = df_all[~df_all.index.isin(final_df.index)]

# Pick 50 random dialogues for test
df_test = df_unused.sample(n=50, random_state=42)

# Test file must have only one column named 'dialogue'
df_test = df_test[["dialogue"]]

df_test.to_csv("data/test.csv", index=False)




