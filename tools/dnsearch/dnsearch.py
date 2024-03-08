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
        print(f"Name: {l.name}\nRegistrar: {l.registrar}\nRegistrant: {l.registrant}\nCreation Date: {l.creation_date}\nLast Updated: {l.last_updated}\nExpiration Date: {l.expiration_date}\nName Servers: {l.name_servers}\nDNSSEC: {l.dnssec}\nDomain Statuses: {l.statuses}\nEmails: {l.emails}")
    except:
        print(f"Lookup failed for: {to_query}")
        exit
    print("-+"*40)

def dns_resolver_query():    
    print("=== DNS Resolver Query ===")
    try:
        for r in dns.resolver.resolve(to_query, 'A'):
            print(f"Target A Record: {r.to_text()}")
    except:
        print(f"No A record found for: {to_query}")

    try:
        for r in dns.resolver.resolve(to_query, 'CNAME'):
            print(f"Target CNAME: {r.target}")
    except:
        print(f"No CNAME found for: {to_query}")

    try:
        mx_test = dns.resolver.resolve(to_query, 'MX')
        for r in mx_test:
            print(f"Target MX Record: {r.exchange.text()}")
    except:
        print(f"No MX record found for: {to_query}")

def lookupresults():
    print("-+"*40)
    print("=== NsLookup Results ===")
    lookup = Nslookup(dns_servers=["1.1.1.1"], verbose=False)
    record = lookup.dns_lookup(to_query)
    record_response = record.response_full
    record_answer= record.answer
    for line in record_response:
        print(f"Record Response: {line}")
    for line in record_answer:
        print(f"Record Answer: {line}")
    print("+-"*40)

who_is_results()
dns_resolver_query()
lookupresults()