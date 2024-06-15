import string
import random

def random_string(length):
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def load_answers():
    answers = {}
    with open("./data/answers.txt", "r") as file:
        for line in file.read().splitlines():
            answer = line.split(":")
            answers[answer[0]] = answer[1]
    return answers

def write_answers(saved_answers, answers):
    previous_questions = saved_answers.keys()
    with open("./data/answers.txt", "a+") as file:
        for question, answer in answers.items():
            if question not in previous_questions:
                file.write(question + ":" + answer + "\n")

def rewrite_answer_file(saved_answers):
    with open("./data/answers.txt", "w+") as file:
        for question, answer in saved_answers.items():
            file.write(question + ":" + answer + "\n")

def remove_answers(saved_answers, answers):
    previous_questions = saved_answers.keys()
    for question in answers.keys():
        if question in previous_questions:
            saved_answers.pop(question)
    rewrite_answer_file(saved_answers)