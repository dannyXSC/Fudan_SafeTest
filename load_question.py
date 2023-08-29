import os

from dataset_loader import default_load, local_load, web_load
from environment import question_path
from question_engine import question_list_merge, save_question_list

if __name__ == "__main__":
    question_result = []
    if os.path.exists(question_path):
        question_list_merge(question_result, local_load(question_path))
    question_list_merge(question_result, web_load())
    save_question_list(question_result, question_path)
