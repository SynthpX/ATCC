import re
import csv
import os
from collections import defaultdict
import unicodedata
import string

def clean_non_english(text):
    cleaned_text = ''.join(c for c in text if unicodedata.category(c).startswith('L') or c.isspace())
    return cleaned_text.strip()

def clean_text(text):
    cleaned_text = re.sub(r'{[^}]*}', '', text)  # Remove formatting tags
    cleaned_text = re.sub(r'\[[^\]]*\]', '', cleaned_text)  # Remove inline comments
    cleaned_text = ''.join(c for c in cleaned_text if c not in string.punctuation)  # Remove punctuation
    return cleaned_text.strip()

def read_ass_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    
    dialogue_pattern = re.compile(r'Dialogue:\s\d+,\d+:\d+:\d+.\d+,\d+:\d+:\d+.\d+,Default,([\w\s]+),\d+,\d+,\d+,,(.*)', re.MULTILINE)
    matches = dialogue_pattern.findall(content)
    
    cleaned_matches = [(char, clean_non_english(clean_text(text))) for char, text in matches]
    return cleaned_matches

def read_csv_file(file_path):
    data = []
    if not os.path.exists(file_path):
        return data

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            data.append((row[0], row[1]))
    return data

def update_csv_data(csv_data, ass_data):
    for character, text in ass_data:
        if csv_data and csv_data[-1][0] == character:
            csv_data[-1] = (character, f"{csv_data[-1][1]} {text}")
        else:
            csv_data.append((character, text))
    return csv_data

def write_csv_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Character', 'Text'])  # Write the header row

        for character, text in data:
            csv_writer.writerow([character, text])

def process_all_ass_files(folder_path, csv_file_path):
    # Read the existing .csv file or create an empty dictionary if the file does not exist
    csv_data = read_csv_file(csv_file_path)

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is an .ass file
        if file_name.endswith('.ass'):
            ass_file_path = os.path.join(folder_path, file_name)
            ass_data = read_ass_file(ass_file_path)
            csv_data = update_csv_data(csv_data, ass_data)

    # Write the updated data back to the .csv file
    write_csv_file(csv_file_path, csv_data)

folder_path = 'ass_folder'
csv_file_path = 'output.csv'
process_all_ass_files(folder_path, csv_file_path)