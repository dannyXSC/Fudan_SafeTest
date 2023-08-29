import json
from typing import List

from question import Question


def question_list_merge(a: List[Question], b: List[Question]):
    # merge to a
    a_set = {question.stem: question for question in a}
    for question in b:
        if question.stem not in a_set:
            a.append(question)


def save_question_list(question_list: List[Question], path):
    with open(path, 'w') as f:
        f.write(json.dumps([question.to_dict() for question in question_list]))


def load_question_list(path):
    with open(path, 'r', encoding='utf8') as f:
        question_list_json = json.loads(f.read())
    return [Question.from_dict(question) for question in question_list_json]
