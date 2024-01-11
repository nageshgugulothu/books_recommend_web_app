import os
import sys
import pandas as pd
import numpy as np
import pickle

from src.logger import logging
from src.exception import CustomException


def save_model(file_path, *objs):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(tuple(objs), file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def load_model(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        logging.error(f"Error occurred while loading model from {file_path}: {e}")
        raise CustomException(e, sys)


def evaluate_model(file_path, result_obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(result_obj, file_obj)

    except Exception as e:
        logging.error(f"Error occurred while evaluating model and saving result to {file_path}: {e}")
        raise CustomException(e, sys)


