#!/usr/bin/env python3
#Author: contrxl
#NotePad++ Snooper
#Snoops on unsaved files stored in \backup, outputs contents in plaintext.
#NOTE: THIS WILL NOT WORK ON ANY *SAVED* FILES, THEY ARE NOT CACHED.
#Provides file name, file path, file creation date and file contents.
# Usage: python3 np-snooper.py

import os
import glob

#Define AppData\Roaming and the relative path to the \backup folder to read from.
app_data_roaming = os.environ['APPDATA']
folder_to_read = r"Notepad++\backup"

#Define the full path to the \backup folder to read from.
full_path = os.path.join(app_data_roaming, folder_to_read)
list_of_files = glob.glob(os.path.join(full_path, '*@*'))

#Iterate through each file in \backups, outputting file name, full file path, file creation date and file contents.
for full_filepath in list_of_files:
    filename = os.path.basename(full_filepath)
    with open(full_filepath, 'rb') as filp:
        contents = filp.read()
        print("-+"*40)
        print(f"{filename = }")
        print(f"{full_filepath = }")
        date = full_filepath.split("@")
        print(f"file_created_on = {date[1]}")
        print(f"file_contents:\n {contents.decode('utf-8')}")
        print("+-"*40)