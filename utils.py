import json
import os
import random
from pathlib import Path

from config import BASE_DIR

QUIZ_FILE = BASE_DIR.joinpath('quiz_question')


def write_json_by_file(path: str) -> None:
    dirs = os.listdir(path)[:30]
    questions = []
    answers = []
    data = {}
    for file in dirs:
        with open(f'{path}/{file}', 'r', encoding='KOI8-R') as f, open('BotForQuiz/questions.json', 'w', encoding='UTF-8') as fw:
            quiz = f.read()
            qa = quiz.split('\n\n')
            for trivia in qa:
                if trivia.startswith('Вопрос'):
                    questions.append(trivia[10:].rstrip())
                elif trivia.startswith('Ответ:'):
                    answers.append(trivia[6:].rstrip())
            for question, answer in zip(questions, answers):
                data[question] = answer
            json.dump(data, fw, ensure_ascii=False)


def get_questions(file) -> dict:
    with open(f'{file}', 'r', encoding='UTF-8') as f:
        return json.load(f)


def get_random_question(dictionary) -> str:
    return random.choice(list(dictionary.keys()))


write_json_by_file(QUIZ_FILE)
