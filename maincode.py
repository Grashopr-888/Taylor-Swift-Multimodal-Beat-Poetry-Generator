import numpy
import csv
import glob
import pandas as pd

path = "Data"

data_files = glob.glob(path +"\*.csv")
print(data_files)