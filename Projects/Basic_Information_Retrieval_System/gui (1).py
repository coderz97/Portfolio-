'''
CS665, Summer24  Project 

Sreya Jain Tobji

'''


import tkinter as tk
from tkinter import filedialog, ttk
import re
import  convert
import  tokenization







# ----------------------------------------Functions-----------------------------------

#Functions to be used in tab1
#for user to select pdf file
def select_file():
    file_path = filedialog.askopenfilename()
    #display the filename
    file_name = file_path.split("/")[-1] if file_path else "None"
    file_label.config(text="Uploaded PDF File: " + file_name)
    #converting pdf to text files
    convert.convert(file_path,"./doc" )

    if file_path:
        print("Selected file:", file_path)
        word_listbox.bind("<ButtonRelease-1>", word_clicked)
    else:
        print("No file selected")



#Functions to be used in tab2
def get_doc_ids_for_word(word):
    inverted_index = tokenization.term_index
    return inverted_index.get(word, [])


def word_clicked(event):
    if word_listbox.curselection():
        selected_word = word_listbox.get(word_listbox.curselection())
        # Retrieve the frequency, document IDs, and Soundex code for the selected word from term_index of tokenization.py
        word_info = tokenization.term_index.get(selected_word, {"Frequency": 0, "Doc ids": "", "Soundex": ""})
        frequency = word_info.get("Frequency", 0)
        doc_ids = word_info.get("Doc ids", "").split(", ") if word_info.get("Doc ids", "") else []
        soundex_code = word_info.get("Soundex", "")
        
        # Clear the text widget and display frequency, Soundex code, and document IDs
        doc_ids_text.delete(1.0, tk.END)
        doc_ids_text.insert(tk.END, f"Frequency: {frequency}\n")
        doc_ids_text.insert(tk.END, f"Soundex: {soundex_code}\n")
        doc_ids_text.insert(tk.END, "Document IDs:\n")
        for doc_id in doc_ids:
            doc_ids_text.insert(tk.END, f"{doc_id}\n")
    else:
        # Clear the text widget if no word is selected
        doc_ids_text.delete(1.0, tk.END)


def search_word():
    search_term = search_entry.get().strip().lower()
    word_listbox.delete(0, tk.END)
    if search_term:
        for word in tokenization.term_index:
            if search_term in word.lower():
                word_listbox.insert(tk.END, word)
    else:
        # If search term is empty, display full list of words
        for word in tokenization.term_index:
            word_listbox.insert(tk.END, word)



def clear_search():
    # Function to clear the search entry and display full list of words
    search_entry.delete(0, tk.END)
    search_word()




#Functions to be used in tab3
def generate_report():
    selected_option = report_option.get()
    report_text.delete(1.0, tk.END)  # Clear any previous content in the report_text
    
    if selected_option == "Document-wise Report":
        report_text.insert(tk.END, "Document-wise Report\n")
        report_data = tokenization.report
        
        # Sort the document IDs
        sorted_doc_ids = sorted(report_data.keys(), key=lambda x: (int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf')))


        
        # Insert data into the report_text in sorted order
        for doc_id in sorted_doc_ids:
            data = report_data[doc_id]
            total_words = data["total_words"]
            num_distinct_words = data["num_distinct_words"]
            report_text.insert(tk.END, f"{doc_id}: Total Words - {total_words}, Distinct Words - {num_distinct_words}\n")
    
    elif selected_option == "Collection-wise Report":
        report_text.insert(tk.END, "Collection-wise Report\n")
        
        # Calculate collection-wise statistics
        total_collection_words = tokenization.tcw
        num_distinct_words_collection = tokenization.dcw
        # Display collection-wise statistics
        report_text.insert(tk.END, f"Total Number of Words in Collection: {total_collection_words}\n")
        report_text.insert(tk.END, f"Number of Distinct Words in Collection: {num_distinct_words_collection}\n")
    
    elif selected_option == "Frequency Report":
        report_text.insert(tk.END, "Frequency Report\n")
        # Fetch most frequent, top 100th, 500th, and 1000th most-frequent words and their frequencies
        most_frequent_word, most_frequent_frequency = tokenization.find_top_n_words(tokenization.freq_index, 1)
        top_100th_word, top_100th_frequency = tokenization.find_top_n_words(tokenization.freq_index, 100)
        top_500th_word, top_500th_frequency = tokenization.find_top_n_words(tokenization.freq_index, 500)
        top_1000th_word, top_1000th_frequency = tokenization.find_top_n_words(tokenization.freq_index, 1000)
        
        # Display the fetched data
        report_text.insert(tk.END, f"Most frequent word: {most_frequent_word}, Frequency: {most_frequent_frequency}\n")
        report_text.insert(tk.END, f"Top 100th word: {top_100th_word}, Frequency: {top_100th_frequency}\n")
        report_text.insert(tk.END, f"Top 500th word: {top_500th_word}, Frequency: {top_500th_frequency}\n")
        report_text.insert(tk.END, f"Top 1000th word: {top_1000th_word}, Frequency: {top_1000th_frequency}\n")
    
    
    else:
        report_text.insert(tk.END, "Invalid option selected for report generation")



def display_inverted_index():
    inverted_index = tokenization.term_index
    inverted_index_text.delete(1.0, tk.END)
    
    # Sort the terms alphabetically
    sorted_terms = sorted(inverted_index.keys())
    
    # Display the inverted index with sorted terms
    for term in sorted_terms:
        info = inverted_index[term]
        doc_ids = info["Doc ids"]
        #frequency = info["Frequency"]
        inverted_index_text.insert(tk.END, f"Term: {term}\n")
        inverted_index_text.insert(tk.END, f"Document IDs: {doc_ids}\n")
        #inverted_index_text.insert(tk.END, f"Frequency: {frequency}\n\n")



#Function to be used in tab5
def tokenizer():
    tokenizer = tokenization.report
    tokenizer_text.delete(1.0, tk.END)  # Clear the existing content
    
    # Sort the document IDs
    sorted_doc_ids = sorted(tokenizer.keys(), key=lambda x: (int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf')))

    # Display the sorted content in the text widget
    for filename in sorted_doc_ids:
        data = tokenizer[filename]
        tokenizer_text.insert(tk.END, f"File: {filename}\n")
        tokenizer_text.insert(tk.END, "Tokens:\n")
        tokenizer_text.insert(tk.END, f"{data['tokens']}\n")
        tokenizer_text.insert(tk.END, "\n")



#-----------------------------------configuring gui-------------------------------------------

window = tk.Tk()
window.title("Information Retrieval System")


notebook = ttk.Notebook(window)

tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)
tab4 = tk.Frame(notebook)
tab5 = tk.Frame(notebook)

notebook.add(tab1, text="UPLOAD")
notebook.add(tab2, text="WORDS")
notebook.add(tab3, text="REPORTS")
notebook.add(tab4, text="INVERTED INDEX")
notebook.add(tab5, text="TOKENIZER")

notebook.pack(expand=True, fill="both")

#----------------------------------Configuring tab1 (pdf upload)-------------------------------------
tk.Label(tab1, text="UPLOAD YOUR PDF FILE:", width=50, height=25).pack()
file_label = tk.Label(tab1, text="Uploaded PDF File: None", fg='black')
file_label.pack()
select_button = tk.Button(tab1, text="Browse", command=select_file, fg='black', bg='#444444')
select_button.pack(pady=5)


#-----------------------------------Configuring tab2 (word search)------------------------------------

tab2_left = tk.Frame(tab2)  
tab2_right = tk.Frame(tab2)
tab2_left.grid(row=0, column=0, sticky="nsew")
tab2_right.grid(row=0, column=1, sticky="nsew")

# Search Box
search_frame = tk.Frame(tab2_left)
search_frame.pack(pady=5)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)
search_button = tk.Button(search_frame, text="Search", command=search_word)
search_button.pack(side=tk.LEFT)
clear_button = tk.Button(search_frame, text="Clear", command=clear_search)
clear_button.pack(side=tk.LEFT)

# Sort the words alphabetically
sorted_words = sorted(tokenization.term_index.keys())

word_listbox = tk.Listbox(tab2_left, selectmode=tk.SINGLE)
word_listbox.pack(fill=tk.BOTH, expand=True)
for word in sorted_words:
    word_listbox.insert(tk.END, word)
word_listbox.bind("<ButtonRelease-1>", word_clicked)

tk.Label(tab2_right, text="Document IDs", fg='black').pack()
doc_ids_text = tk.Text(tab2_right)
doc_ids_text.pack(fill=tk.BOTH, expand=True)




#---------------------------------------Configuring tab3 (Reports)------------------------------
report_option_label = tk.Label(tab3, text="Select Report Type:", fg='black')
report_option_label.pack()

report_option = ttk.Combobox(tab3, values=["Document-wise Report", "Collection-wise Report", "Frequency Report"])
report_option.pack()

#Button to generate report
generate_button = tk.Button(tab3, text="Generate Report", command=generate_report)
generate_button.pack()

#Text widget to display report
report_text = tk.Text(tab3, height=20, width=100)  # Increase height and width
report_text.pack(pady=10, side="left", fill="both", expand=True)  # Adjust pack options

#Scrollbar for report_text
scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=report_text.yview)
scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))  # Adjust packing options
report_text.configure(yscrollcommand=scrollbar.set)


#-----------------------------Configuring tab4 (Inverted Index)------------------------
# Button to display inverted index
display_index_button = tk.Button(tab4, text="Display Inverted Index", command=display_inverted_index)
display_index_button.pack()

# Text widget to display inverted index
inverted_index_text = tk.Text(tab4, height=20, width=100)
inverted_index_text.pack(pady=10, side="left", fill="both", expand=True)

# Scrollbar for inverted index text
inverted_index_scrollbar = ttk.Scrollbar(tab4, orient="vertical", command=inverted_index_text.yview)
inverted_index_scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
inverted_index_text.configure(yscrollcommand=inverted_index_scrollbar.set)


#--------------------------------Configuring tab5 (tokenizer)--------------------------------
# Button to display tokenizer
display_index_button = tk.Button(tab5, text="Display result of tokenizer", command=tokenizer)
display_index_button.pack()

# Text widget to display tokenizer
tokenizer_text = tk.Text(tab5, height=20, width=100)
tokenizer_text.pack(pady=10, side="left", fill="both", expand=True)

# Scrollbar for tokenizer text
tokenizer_scrollbar = ttk.Scrollbar(tab5, orient="vertical", command=tokenizer_text.yview)
tokenizer_scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
tokenizer_text.configure(yscrollcommand=tokenizer_scrollbar.set)


window.mainloop()
