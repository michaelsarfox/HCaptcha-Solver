An bot to solve HCaptcha's text-free-entry challenges using GPT-3.5

This can be used wihtout proxies, but residential proxies are preferred (higher success rates)

**Usage**
* Open main.py and replace the following
	* Replace site_url with the captcha site_url param
 	* * Replace captcha_url with the url of site where captcha is loaded.
 
**Run**
* Run app.py for HSW (fingerprint) generation
* Run main.py to test solve captcha

**IMPORTANT**
* Captcha submissions are flagged due to the following:
	* HSW fingerprint being generated improperly. Requires a real encrypted fingerprint payload with AES-GCM-256
	* Motion data is not developed fully. 
