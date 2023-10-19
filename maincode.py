import numpy
import csv
import glob
import pandas as pd

path = "Data"

data_files = glob.glob(path +"\*.csv")
#print(data_files)

#lists
all_dataframes = []
lyric_list = []

# open each file and add it to the dataframes list
for file in data_files:
    #print(file) #check if all files are in there
    all_dataframes.append(pd.read_csv(file))
    
res = pd.concat(all_dataframes) #all dataframes merged into one

#list with all the lyrics
lyric_list = res["lyric"].tolist()


