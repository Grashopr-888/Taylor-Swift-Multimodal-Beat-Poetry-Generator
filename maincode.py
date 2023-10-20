import numpy
import csv
import glob
import pandas as pd
import re

# word package
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import brown
#download the brown corpus
nltk.download('brown')

#set language to english for the stemmer
stemmer = SnowballStemmer('english')

# ------ 1. RETRIEVE DATA ------
data_path = "Data"
midnights_path = "Midnights"
vault_path = "TheVault"

data_files = glob.glob(data_path +"\*.csv")
mid_txt_files = glob.glob(midnights_path + "\*.txt")
vault_txt_files = glob.glob(vault_path + "\*.txt")

#print(data_files)

# lists
all_dataframes = []
lyric_list = []

# open each file and add it to the dataframes list
for file in data_files:
    #print(file) #check if all files are in there
    all_dataframes.append(pd.read_csv(file))
    
res = pd.concat(all_dataframes) #all dataframes merged into one

lyric_list = res["lyric"].tolist() # list with all the lyrics

# open each file and add it to lyric_list (midnights album)
for txt_file in mid_txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()  # splitting by lines
        for line in lines:  # to add every string/line and not the entire list
            lyric_list.append(line)  # adding the midnights lyrics

# open each file and add it to lyric_list (from the vault tracks)
for txt_file in vault_txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()  # splitting by lines
        for line in lines:  # to add every string/line and not the entire list
            lyric_list.append(line)  # adding the midnights lyrics


#print(lyric_list)

df_all_lyrics = pd.DataFrame(lyric_list, columns=['Lyrics'])
print(df_all_lyrics)

# ------ 2. PREPROCESSING ------

# return the base of words
def str_stemmer(s):

    return s.lower()

def units_chars(s):
	# replacing special characters with whitespaces
	if isinstance(s, str):
		s = s.replace("/"," ")
		s = s.replace("\\"," ") # deletes single \ from string
		s = s.replace("//"," ")
		s = s.replace("-"," ")
		s = s.replace("#"," ")
		s = s.replace("."," ")
		s = s.replace("("," ")
		s = s.replace(")"," ")
		s = s.replace("%"," ")
		s = s.replace("!"," ")
		s = s.replace("$"," ")
		s = s.replace("&"," ")
		s = s.replace(","," ")
        # s = s.replace("'"," ")
		# s = s.replace('"',"")
		return s


def replace_contractions(s):
    # replacing contractions
    contractions_patterns = [
        (r"won\'t", "will not"),
        (r"can\'t", "cannot"),
        (r"i\'m", "i am"),
        (r"ain\'t", "is not"),
        (r"(\w+)\'ll", "\g<1> will"),
        (r"(\w+)n\'t", "\g<1> not"),
        (r"(\w+)\'ve", "\g<1> have"),
        (r"(he|she|it|that|there|who)\'s", "\g<1> is"), # distinguishing between contractions and possessives
        (r"(\w+)\'re", "\g<1> are"),
        (r"(\w+)\'d", "\g<1> would")
    ]
    
    for pattern, replacement in contractions_patterns:
        s = re.sub(pattern, replacement, s)
    
    return s

# replace the contractions within the lyrics 
df_all_lyrics['Lyrics'] = df_all_lyrics['Lyrics'].apply(replace_contractions)

     
#apply stemmer to dataframe for columns: search_term, product_title, and product_description
df_all_lyrics['Lyrics'] = df_all_lyrics['Lyrics'].map(lambda x:str_stemmer(x))

#delete special characters
df_all_lyrics['Lyrics'] = df_all_lyrics['Lyrics'].map(lambda x:units_chars(x))

print(df_all_lyrics)


