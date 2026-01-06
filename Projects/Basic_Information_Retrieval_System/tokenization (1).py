'''
CS665, Summer24  Project 

Sreya Jain Tobji

'''

import os
import nltk
import string
import re
from collections import defaultdict, Counter
nltk.download('punkt')  #module punkt provides a pre-trained model for tokenizing text into words
from nltk.tokenize import word_tokenize



# Initialize variables
total_collection_words = 0
distinct_words_set = set() 
num_distinct_words_collection=0
term_frequency = defaultdict(int)
tokenized_files = {}        # Initialize a dictionary to store tokenized words along with the file they belong to

# Path to the folder containing converted text files
folder_path = "./doc"




def soundex(term):
    # Define the Soundex mapping
    soundex_mapping = {
        'b': 1, 'f': 1, 'p': 1, 'v': 1,
        'c': 2, 'g': 2, 'j': 2, 'k': 2, 'q': 2, 's': 2, 'x': 2, 'z': 2,
        'd': 3, 't': 3,
        'l': 4,
        'm': 5, 'n': 5,
        'r': 6
    }

    # Initialize Soundex code with the first letter of the term
    term = term.lower()
    soundex_code = term[0]

    # Remove non-alphabet characters and replace vowels with '0'
    term = term[1:].replace('a', '').replace('e', '').replace('i', '').replace('o', '').replace('u', '').replace('y', '')

    # Encode the remaining letters using the Soundex mapping
    for char in term:
        soundex_digit = soundex_mapping.get(char)
        if soundex_digit is not None:
            # Ignore consecutive digits
            if soundex_digit != soundex_code[-1]:
                soundex_code += str(soundex_digit)

        # Stop encoding when the Soundex code length is 4 characters
        if len(soundex_code) == 4:
            break

    # Pad or truncate the Soundex code to ensure it's 4 characters long
    soundex_code = soundex_code.ljust(4, '0')

    return soundex_code

#function to create two inverted indexes, one sorted alphabetically by terms and second sorted by term frequency
from collections import defaultdict, Counter

def create_inverted_index(data):
    # Initializing two inverted indexes with terms and corresponding posting list and frequency of the term
    term_inverted_index = defaultdict(lambda: {"documents": [], "tf": 0, "soundex": ""}) 
    frequency_inverted_index = defaultdict(lambda: {"documents": [], "tf": 0, "soundex": ""})  
    
    for filename, file_data in data.items():
        tokens = file_data["tokens"] 
        term_occurrences = file_data["term_occurrences"]  # Retrieve term occurrences
        
        # Calculating the frequency of occurrences of each term using a counter
        term_frequency = Counter(tokens) 
        for term, frequency in term_frequency.items():
            term_inverted_index[term]["documents"].append((filename, frequency))
            term_inverted_index[term]["tf"] += frequency
            frequency_inverted_index[term]["documents"].append((filename, frequency))
            frequency_inverted_index[term]["tf"] += frequency
            # Calculate Soundex code for the term and store it in the inverted index
            term_inverted_index[term]["soundex"] = soundex(term)
            frequency_inverted_index[term]["soundex"] = soundex(term)
    
    # Inverted index sorted alphabetically by terms
    term_sorted_index = {}
    for term, info in term_inverted_index.items():
            term_sorted_index[term] = {
                "Doc ids": ', '.join([f"{doc[0]} ({doc[1]})" for doc in info["documents"]]),
                "Frequency": info["tf"],
                "Soundex": info["soundex"],
                "Term Occurrences": info["documents"]
            }

    # Inverted index sorted by term frequency
    frequency_sorted_index = {}
    for term, info in frequency_inverted_index.items():
            frequency_sorted_index[term] = {
                "Doc ids": ', '.join([f"{doc[0]} ({doc[1]})" for doc in info["documents"]]),
                "Frequency": info["tf"],
                "Soundex": info["soundex"],
                "Term Occurrences": info["documents"]
            }

    return term_sorted_index, frequency_sorted_index



# Function to find the top nth most-frequent word and its frequency from the freq_index
def find_top_n_words(index, n):
    sorted_index = sorted(index.items(), key=lambda x: x[1]['Frequency'], reverse=True)
    if n <= len(sorted_index):
        word, info = sorted_index[n - 1]
        return word, info['Frequency']
    else:
        return None, None





#---------------------------------tokenization----------------------------------------

import chardet

# Loop over each file in the folder to normalize the words in it
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # Determine the encoding of the file
    with open(file_path, 'rb') as file:
        encoding = chardet.detect(file.read())['encoding']

    # Read the file using the detected encoding
    with open(file_path, 'r', encoding=encoding) as file:
        text = file.read()
    #with open(file_path, "r", encoding="utf-8") as file:
        #text = file.read()

        # Remove all special characters, punctuation, numbers, and various types of brackets
        text = re.sub(r'[^A-Za-z\s]', '', text)
        text = re.sub(r'[\[\]{}()<>]', '', text)

        # Case folding
        text = text.lower()

        # Tokenization
        tokens = word_tokenize(text)

        # Calculate term occurrences
        term_occurrences = Counter(tokens)

        # Calculating document-wise statistics
        num_distinct_words = len(set(tokens))
        total_words = len(tokens)

        # Store tokenized words, total words, and distinct words in the dictionary
        tokenized_files[filename] = {
            "tokens": tokens,
            "total_words": total_words,
            "num_distinct_words": num_distinct_words,
            "term_occurrences": term_occurrences
        }



# to print tokenized words and statics for each document
for filename, data in tokenized_files.items():
        #print document wise report in terminal
        print(f"File: {filename}")
        print("Tokens:", data["tokens"])
        '''
        print("Tokens and frequencies:")
        word_frequency = Counter(data["tokens"])
        for word, frequency in word_frequency.items():
            print(f"\t{word}: {frequency}")
        '''
        print(f"Total number of words: {data['total_words']}")
        print(f"Number of distinct words: {data['num_distinct_words']}")
        print()

        #to calculate collection wise report 
        total_collection_words += data["total_words"]
        distinct_words_set.update(data["tokens"])
        num_distinct_words_collection = len(distinct_words_set)



#-----------------------------------------inverted index------------------------------------------

# Create inverted index 
term_index,freq_index = create_inverted_index(tokenized_files)
report = tokenized_files

# Print the sorted index
for term, info in term_index.items():
    print(f"term: {term}")
    print(f"Doc ids: {info['Doc ids']}")
    print(f"Frequency: {info['Frequency']}")
    print(f"Soundex: {info['Soundex']}")
    print()

#---------------------------------------statics-----------------------------------------------


print("Total number of words in the collection:", total_collection_words)
print("Number of distinct words in the collection:", num_distinct_words_collection)
print()

tcw=total_collection_words
dcw=num_distinct_words_collection


# Find the most frequent, top 100th, 500th, and 1000th most-frequent words and their frequencies
most_frequent_word, most_frequent_frequency = find_top_n_words(freq_index, 1)
top_100th_word, top_100th_frequency = find_top_n_words(freq_index, 100)
top_500th_word, top_500th_frequency = find_top_n_words(freq_index, 500)
top_1000th_word, top_1000th_frequency = find_top_n_words(freq_index, 1000)

# Print the collection statics 
print("Most frequent word:", most_frequent_word, "Frequency:", most_frequent_frequency)
print("Top 100th word:", top_100th_word, "Frequency:", top_100th_frequency)
print("Top 500th word:", top_500th_word, "Frequency:", top_500th_frequency)
print("Top 1000th word:", top_1000th_word, "Frequency:", top_1000th_frequency)
