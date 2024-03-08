import sys
import whois
from nslookup import Nslookup
import dns.resolver


to_query = sys.argv[1]

def who_is_results():
    print("+-"*40)
    print("=== WhoIs Results ===")
    try:
        l = whois.query(to_query)
        print(l.dnssec)
    except:
        print(f"Lookup failed for: {to_query}")
        exit
    print("-+"*40)

who_is_results()