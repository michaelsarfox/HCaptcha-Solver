import tls_client

def create_client(proxy):
    client = tls_client.Session(client_identifier = "chrome_122")
    client.headers = get_headers()
    client.timeout_seconds = 99999
    if proxy:
        client.proxies = {"http": "http://" + proxy, "https": "https://" + proxy}
    return client

def get_headers():
    return {
        "Connection": "keep-alive",
        "Sec-Ch-UA": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Sec-Ch-UA-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Sec-Ch-UA-Platform": '"Windows"',
        "Origin": "https://newassets.hcaptcha.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://newassets.hcaptcha.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "hmt_id=c87757f2-e88a-4ace-98fb-d23edeb34dfb; __cflb=0H28vk2VKwPbLoawFincekpozDKK5F2ckohieevzWSy"
    }
