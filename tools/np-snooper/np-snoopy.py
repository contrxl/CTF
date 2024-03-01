import os
import glob

app_data_local = os.environ['LOCALAPPDATA']
relative_path_to_bin = r"Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\TabState"
complete_path = os.path.join(app_data_local, relative_path_to_bin)

bin_list = glob.glob(os.path.join(complete_path, '*.bin'))


for bins in bin_list:
    bad = ['.0.bin', '.1.bin']
    if bad[0] in bins or bad[1] in bins:
        continue
    filename = os.path.basename(bins)
    
    with open(bins, 'rb') as flip:
        contents = flip.read()
        magic_bytes = contents[0:3]
        #file_path = contents[5:contents.index(b'\x32')]
        path_length = contents[4]
        file_path = contents[5:5+path_length*2]
        file_path = file_path.decode('utf-16')
    
        #pre_text_buffer = b"%s\x01\x00\x00\x00%s"
        #content_test = contents.find(pre_text_buffer)
        special_bytes = contents.index(b'\x01\x00\x00\x00')
        file_char_count = contents[special_bytes+4]

        actual_file_content = contents[special_bytes+5:-5]
        actual_file_content = actual_file_content.decode('utf-16')

        print("+-"*40)       
        print(f"{filename = }")
        print(f"{file_char_count = }")
        print(f"{file_path = }")
        print(f"{actual_file_content = }")
        print("-+"*40)