import glob
import pandas as pd
import re
import random

#Additional import for Markov Chain
from collections import defaultdict

#Word package
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import brown
from nltk.corpus import words
from nltk.corpus import cmudict


#Download the corpus
#nltk.download('brown')
#nltk.download('words')
#nltk.download('cmudict')

brown_words = set(i.lower() for i in brown.words())
word_set = set(i.lower for i in words.words())

#Dictionaries
pronouncing_dict = cmudict.dict()
english_words = set(words.words())

#Set language to english for the stemmer
stemmer = SnowballStemmer('english')


# ------ 1. RETRIEVE DATA ------
data_path = "Data"
midnights_path = "Midnights"
vault_path = "TheVault"

data_files = glob.glob(data_path +"\*.csv")
mid_txt_files = glob.glob(midnights_path + "\*.txt")
vault_txt_files = glob.glob(vault_path + "\*.txt")

#Lists
all_dataframes = []
lyric_list = []
lyric_word_set = set()

#Open each file and add it to the dataframes list
for file in data_files:
    all_dataframes.append(pd.read_csv(file))
    
res = pd.concat(all_dataframes) #all dataframes merged into one

lyric_list = res["lyric"].tolist() #list with all the lyrics

#Open each file and add it to lyric_list (midnights album)
for txt_file in mid_txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()  #splitting by lines
        for line in lines:  #to add every string/line and not the entire list
            lyric_list.append(line)  #adding the midnights lyrics

#Open each file and add it to lyric_list (from the vault tracks)
for txt_file in vault_txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()  #splitting by lines
        for line in lines:  #to add every string/line and not the entire list
            lyric_list.append(line)  #adding the midnights lyrics

df_all_lyrics = pd.DataFrame(lyric_list, columns=['Lyrics'])


# ------ 2. PREPROCESSING ------
#Return the base of words
def str_stemmer(s):
    return s.lower()

def units_chars(s):
    #Replacing special characters with whitespaces
    if isinstance(s, str):
        s = s.replace("/", " ") #deletes single / from string
        s = s.replace("\\", " ")  
        s = s.replace("//", " ")
        s = s.replace("-", " ")
        s = s.replace("\"", " ")
        s = s.replace(".", " ")
        s = s.replace("(", " ")
        s = s.replace(")", " ")
        s = s.replace("%", " ")
        s = s.replace("!", " ")
        s = s.replace("?", " ")
        s = s.replace("&", " ")
        s = s.replace(",", " ")
        s = s.replace('"', " ")
        s = s.replace('—', " ")
        s = s.replace(';', " ")
        s = s.replace(':', " ")
        s = s.replace('…', " ")
        s = s.replace('–', " ")
        s = s.replace('”', " ")
        #Make sure every ‘ and ’ gets replaced by '
        s = s.replace('’', "'")
        s = s.replace('‘', "'")
       
        return s

     
def replace_contractions(s):
    #Replacing contractions (and typos)
    contractions_patterns = [
        (r"won\'t", "will not"),
        (r"can\'t", "cannot"),
        (r"i\'m", "i am"),
        (r"ain\'t", "is not"),
        (r"(\w+)\'ll", "\g<1> will"),
        (r"(\w+)n\'t", "\g<1> not"),
        (r"(\w+)\'ve", "\g<1> have"),
        (r"(he|she|it|that|there|who|joke|trouble|all|karma|castle|thing)\'s", "\g<1> is"), #distinguishing between some contractions and possessives
        (r"(\w+)\'re", "\g<1> are"),
        (r"(\w+)\'d", "\g<1> would"),
        (r"\'till|til", "until"),
        (r"\'untill", "until"),
        (r"\'cause", "because"),
        (r"gon\'", "gonna"),
        (r"\'tis", "this is"),
        (r"\'cross", "across"),
        (r"\'(\w+)\'", "\g<1>"),
        (r"\'(\w+)", "\g<1>")
    ]
    
    for pattern, replacement in contractions_patterns:
        s = re.sub(pattern, replacement, s)
    
    return s

#Replacing -in' with -ing    
def continuous_verbs(s):
     for word in s.split():
          if ("in'" in word):
                s = re.sub("in'", "ing", s)         
     return s

#Creating a set of all words
def word_set(s):
    for word in s.split():
        lyric_word_set.add(word)

#Apply stemmer to dataframe for columns: search_term, product_title, and product_description
df_all_lyrics['Lyrics'] = df_all_lyrics['Lyrics'].map(lambda x:str_stemmer(x))

#Delete special characters
df_all_lyrics['Lyrics'] = df_all_lyrics['Lyrics'].map(lambda x:units_chars(x))

#Replace the contractions within the lyrics 
df_all_lyrics['Lyrics'] = df_all_lyrics['Lyrics'].map(lambda x:replace_contractions(x))

#Change all continuous -in' verbs to -ing
df_all_lyrics['Lyrics'] = df_all_lyrics['Lyrics'].map(lambda x:continuous_verbs(x))

#Add all distinct words to set
df_all_lyrics['Lyrics'].map(lambda x:word_set(x))
 

#---- 3. MARKOV CHAIN ----
#Create a dictionary for the Markov chain
markov_chain = defaultdict(set) #word pairs

#Make word pairs of words in the lyrics
for lyric in df_all_lyrics['Lyrics']:
    words = lyric.split()
    for i in range(len(words)):
        if i != len(words)-1:
            word = words[i]
            next_word = words[i + 1]
        else:
            next_word = "\n"
        markov_chain[word].add(next_word)

def countSyllables(s):
    num = 0
    
    for word in s:
        if word in pronouncing_dict:
            #Get the first pronunciation and count the number of syllables
            phonemes = pronouncing_dict[word][0]
            
            for p in phonemes:
                if p[-1].isdigit():
                    num += 1
        else:
            num += 2
    
    return num


#---- 4. ALLITERATIONS ----
#Finds alliterations for in the poem
#Inputs word
#Outputs list of alliterations to word
def find_alliterative_words(word):
    phonemes = pronouncing_dict.get(word)

    try:
        initial_phoneme = phonemes[0][0]  #get the initial phoneme
    except TypeError:
        return random.choice(list(markov_chain.keys()))
    
    alliterations = []

    for w in lyric_word_set:
        try:
            word_phonemes = pronouncing_dict.get(w)
        except TypeError:
            continue
        
        #If word phoneme exists and is the same as initial phoneme add it to alliteration list
        if word_phonemes and word_phonemes[0][0] == initial_phoneme:
            alliterations.append(w)

    return alliterations


#---- 5. GENERATE POEM ----
#Function to generate a poem using the Markov chain
def generate_poem(seed_word, poem_length=10, max_s = 80):
    poem = [seed_word]
    current_word = seed_word
    start_new = True
    fw = 0 #first word in the sentence
    sentence_len = 0
    line_nr = 0 #line in poem

    while line_nr < poem_length:
        next_words = markov_chain.get(current_word)

        #Current word has matching word pairs
        if next_words:
            next_words = list(next_words)
            next_word = random.choice(next_words)

        #Otherwise find alliteration  
        if next_word == current_word or not next_words:
            next_words = find_alliterative_words(current_word)
            next_word = random.choice(next_words)
        
        #Check if it is valid to start a new line
        if next_word == "\n" and not start_new:
            if next_words and len(next_words) > 1:
                continue
            else:
                next_words = find_alliterative_words(current_word)

        poem.append(next_word)
        start_new = True

        if next_word != "\n":
            current_word = next_word
            sentence_len = countSyllables(' '.join(poem[fw:])) #current sentence length
            #Check if new sentence should be started
            if sentence_len > max_s:
                start_new = False #next word cannot be "\n"

                fw = len(poem)
                poem.append("\n")
                line_nr += 1
            
        else:
            start_new = False #next word cannot be "\n"
          
            #set maximum sentence length
            if line_nr == 0: #if it's the first sentence, set maximum syllables
                max_s = countSyllables(' '.join(poem[fw:]))
            
            line_nr += 1
            fw = len(poem)

    return ' '.join(poem).replace("\n ", "\n") #make sure new lines don't start with a white space

#Generate a poem with a random seed word
random_seed_word = random.choice(list(markov_chain.keys()))
poem = generate_poem(random_seed_word, poem_length=5, max_s=60)
print(poem)
