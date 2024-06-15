import requests

def create_instance():
    response = requests.post("http://127.0.0.1:5000/create_instance/", json = {
        "site_key": "b2b02ab5-7dae-4d6f-830e-7b55634c888b",
        "site_host": "discord.com",
        "captcha_url": "https://accounts.hcaptcha.com/demo?sitekey=b2b02ab5-7dae-4d6f-830e-7b55634c888b&host=discord.com"
    })
    print(response.text)

def solve():
    response = requests.post("http://127.0.0.1:5000/solve/")
    print(response.text)

if __name__ == "__main__":
    create_instance()
    solve()