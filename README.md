# Overview
This program is a Taylor Swift lyric-based poem generator that combines data files from multiple sources, processes them, and then uses a Markov Chain to generate a poem. The program utilizes various libraries including pandas, and NLTK to handle data manipulation, text processing, and natural language processing.

# System Requirements

## Software Requirements
- Python (3.8 or later).
- pip: A package installer for Python.

## Installing Required Packages
You can install the required packages using pip. Run the following command in your terminal or command prompt:
```
pip install numpy pandas nltk
```

## Installation
1. Ensure that you have Python 3.8 or later installed on your system.
2. Ensure that pip is installed on your system.
3. Download the code or clone the repository to your local machine.
4. Ensure that you have the folders containing the text data ("Data", "Midnights", "TheVault").
5. Navigate to the directory containing the code in your terminal or command prompt.
6. Run the pip command mentioned above to install the required packages.
7. Download the necessary NLTK data by running the following Python commands:
```
nltk.download('brown')
nltk.download('words')
nltk.download('cmudict')
```


# Running the Generator
To run the program, follow these steps:
1. Ensure that your working directory is set to the directory containing the code.
2. Make sure you have your data files in the required format and in the correct directories. The program expects CSV files containing lyrics in a "Data" folder, and text files in the "Midnights" and "TheVault" folders.
3. Run the program using the following command in your terminal or command prompt:
```
python maincode.py
```
4. The program will output a generated poem.

# Data Files
## Directories
- The program expects CSV files containing lyrics in a "Data" directory.
- The program expects text files for the Midnights album in the "Midnights" directory.
- The program expects text files for the vault tracks in "TheVault" directory.
- The directory paths of the data files are stored in variables. To change the path you can edit the follwing:
```
data_path = "Data"
midnights_path = "Midnights"
vault_path = "TheVault"
```
- Ensure that the text and CSV files are encoded in UTF-8 to avoid encoding issues.

## Data Source
- The CSV files in the Data directory were retreived from the "Taylor Swift Song Lyrics (All Albums)" Kaggle dataset by Jan Llenzl Dagohoy. This dataset can be found on: https://www.kaggle.com/datasets/thespacefreak/taylor-swift-song-lyrics-all-albums
- All lyrics are lyrics from Taylor Swift.
