# Information Retrieval


Team:

CS665, S24  Project 

Sreya Jain Tobji
Tirumala Tejaswi Masimukku


--------------------------------------------------------------------------------


How to set up:

1. Open command prompt
 
2. Type:
		 cd 'path of the file containing all the .py scripts'

3. Run the below commands if not already installed:

		pip install PyPDF2
		pip install nltk
		pip install chardet

4. Now run: 
		python gui.py


---------------------------------------------------------------------------------


Table of Contents

There are three python files in the project:

1. gui.py:
This is the main python file that call functions from other python files.
The gui is configured in this file.


2. convert.py
This python file contains the function to split and convert each page of the
uploaded pdf file into separate text documents into the output folder location.


3. tokenization.py
This python file is where most of the computation takes place
each text file in the output folder path is tokenized.
the output of the tokenizer is sent to inverted index
the inverted index function returns two inverted indexes, one sorted alphabetically by tokens and one sorted by term frequency
this python file also contains function to calculate term occurrence, term frequency,
document and collection wise total and distinct words and also find the most frequent, top 100th, 500th, and 1000th most-frequent words.
Function to calculate soundex is also defined here.

------------------------------------------------------------------------------


How to use



1. (Optional) upload the pdf file through tab1

2. (Optional) close the window and run the program again

3. Add any text file to doc folder , close and run "python guy.py" again

4. Browse tab2 to search for words, the overall frequency, soundex and document ids along with the number of occurance of the word in each document will be displayed on right side of tab2 

5. Browse tab 3 to get document wise, collection-wise, frequency reports.

6. From tab 4 you can view the inverted index that is alphabetically sorted.

7. From tab 5 you can view the result of the tokenizer.


--------------------------------------------------------------------------------

Adding new text file to output file location

you can add new files with any name to the output file location, but please ensure to run the program again
the new file will be saved as the last file in the inverted index.




