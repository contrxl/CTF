# Infinite Queue
This challenge is a basic web page with only one options: to sign up to be in a ticket queue. Clicking on "Buy Tickets" takes you to `/queue` where you can enter your email to sign up. Entering your mail and pressing "Sign me up" takes you to queue screen. 

If we inspect the page and look at our cookies, we can see a JWT token for `queue_token`. Fire this token into a JWT decoder like `https://jwt.io` and we see that the token contains:
```json
{
	"user_id": "contrxl@contrxl.io",
	"queue_time": 17881827371.1920,
	"exp": 53434534
}
```
We can try to modify this to change our `"queue_time"` to zero. Doing this changes the queue to "Calculating", and shows us a long error trace. The error trace leaks the JWT secret! Now, we can sign up again, and use the JWT secret to craft a new, valid token with a `queue_time` of one.
After refreshing your queue status, you will be taken to a "Complete Purchase" page, press the button to get the flag!
