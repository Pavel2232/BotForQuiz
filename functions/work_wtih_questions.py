import json
import os
from pathlib import Path


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
            with open(f'{Path(__file__).resolve().parent.parent}/questions.json', 'w', encoding='UTF-8') as fw:
                for question, answer in zip(questions, answers):
                    data[question] = answer
    json.dump(data, fw, ensure_ascii=False)


if __name__ == '__main__':
    write_json_by_file(Path(__file__).resolve().parent.parent.joinpath(os.getenv('QUIZ_DICT')))
