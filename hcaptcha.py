import client
import solver
import body

class HCaptcha:
    def __init__(self, site_key, site_host, proxy = None):
        self.site_key = site_key
        self.site_host = site_host

        self.client = client.create_client(proxy)
        self.version = self.get_version()
        self.solver = solver.Solver()

    def get_version(self):
        return self.client.get("https://hcaptcha.com/1/api.js").text.split("v1/")[1].split("/")[0]

    def get_config(self):
        return self.client.post("https://api2.hcaptcha.com/checksiteconfig?v=" + self.version + "&host=" + self.site_host + "&sitekey=" + self.site_key + "&sc=1&swa=1&spst=1").json()["c"]

    def get_challenge(self, config, rq):
        self.client.headers["Content-Type"] = "application/x-www-form-urlencoded"
        response = self.client.post("https://api.hcaptcha.com/getcaptcha/" + self.site_key, data = body.create_challenge_body(self, config, rq))
        if "generated_pass_UUID" in response.text:
            return response.json()["generated_pass_UUID"]
        elif "tasklist" not in response.text:
            print("ERROR: Failed to get challenge")
            return None
        return self.refresh_challenge(config, response.json(), rq)
        
    def refresh_challenge(self, config, challenge, rq):
        response = self.client.post("https://api.hcaptcha.com/getcaptcha/" + self.site_key, data = body.create_refresh_body(self, config, challenge, rq))
        if "generated_pass_UUID" in response.text:
            return response.json()["generated_pass_UUID"]
        elif "text_free_entry" not in response.text:
            print("[-] Failed to force text challenge")
            return None
        return response.json()
    
    def check_answers(self, config, key, answers):
        self.client.headers["Content-Type"] = "application/json"
        response = self.client.post("https://api.hcaptcha.com/checkcaptcha/" + self.site_key + "/" + key, json = body.create_submission_body(self, config, answers))
        if "generated_pass_UUID" not in response.text:
            return response.json()["c"]
        return response.json()["generated_pass_UUID"]
    
    def solve(self, rq = None):
            config = self.get_config()
            challenge = self.get_challenge(config, rq)
            if isinstance(challenge, dict):
                response = self.solver.solve_challenge(self, config, challenge)
                if isinstance(response, str):
                    return response
            elif isinstance(challenge, str):
                return challenge
            return None
    
if __name__ == "__main__":
    captcha = HCaptcha(site_key = "b2b02ab5-7dae-4d6f-830e-7b55634c888b", site_host = "discord.com")
    captcha.solve()