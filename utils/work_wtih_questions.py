import json
import os
import random

from environs import Env

from config.db import BASE_DIR

env = Env()
env.read_env('.env')

QUIZ_DIR = BASE_DIR.joinpath(env('QUIZ_DIR'))


def write_json_by_file(path: str) -> None:
    dirs = os.listdir(path)[:30]
    questions = []
    answers = []
    data = {}
    for file in dirs:
        with open(f'{path}/{file}', 'r', encoding='KOI8-R') as f:
            quiz = f.read()
            qa = quiz.split('\n\n')
            for trivia in qa:
                if trivia.startswith('Вопрос'):
                    questions.append(trivia[10:].rstrip())
                elif trivia.startswith('Ответ:'):
                    answers.append(trivia[6:].rstrip())
            with open(f'{BASE_DIR}/questions.json', 'w', encoding='UTF-8') as fw:
                for question, answer in zip(questions, answers):
                    data[question] = answer
                json.dump(data, fw, ensure_ascii=False)


def get_questions(file) -> dict:
    with open(f'{file}', 'r', encoding='UTF-8') as f:
        return json.load(f)


def get_random_question(dictionary) -> str:
    return random.choice(list(dictionary.keys()))


if __name__ == '__main__':
    write_json_by_file(QUIZ_DIR)
