import concurrent.futures
import requests
import time
import util

class Solver:
    def __init__(self):
        self.saved_answers = util.load_answers()

    def get_tasks(self, challenge):
        tasks = {}
        for task in challenge["tasklist"]:
            tasks[task["task_key"]] = task["datapoint_text"]["en"]
        return tasks
    
    def is_answered(self, tasks, answers):
        for key, task_question in tasks.items():
            for saved_question, answer in self.saved_answers.items():
                if task_question == saved_question:
                    tasks[key] = {"text": answer}
                    answers[saved_question] = answer
        return all(value == "text" for value in tasks.keys())
    
    def ask_question(self, question):
        return requests.post('https://api.openai.com/v1/chat/completions', headers = {
            "Content-Type": "application/json",
            "Authorization": "PUT KEY HERE"
        }, json = {
            "model": "gpt-3.5-turbo-0125",
            "messages": [{"role": "user", "content": "Strictly answer ONLY with a SINGLE word or NUMBER.\nIf it's a number question do not calculate or apply any operations, just find the number: " + question,}],
            "temperature": 0
            }
        ).json()["choices"][0]["message"]["content"]

    def answer_question(self, tasks, answers, task_key, question):
        answer = self.ask_question(question)
        answers[question] = answer
        tasks[task_key] = {"text": answer}

    def solve_challenge(self, hcaptcha, config, challenge):
        tasks, answers = self.get_tasks(challenge), {}
        if not self.is_answered(tasks, answers):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(lambda args: self.answer_question(tasks, answers, *args), tasks.items())
        time.sleep(1.5)
        return self.submit_answers(hcaptcha, config, challenge["key"], tasks, answers)

    def submit_answers(self, hcaptcha, config, key, tasks, answers):
        response = hcaptcha.check_answers(config, key, tasks)
        if isinstance(response, str) and response.startswith("P1"):
            util.write_answers(self.saved_answers, answers)
            self.previous_answers = util.load_answers()
        elif isinstance(response, dict):
            util.remove_answers(self.saved_answers, answers)
        return response