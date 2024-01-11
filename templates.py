import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(message)s]')

list_of_files = [
    ".github/workflows/main.yaml",
    "src/__init__.py",
    "src/components/__init__.py",
    "src/components/data_ingestion.py",
    "src/components/data_transformation.py",
    "src/components/model_trainer.py",
    "src/exception.py",
    "src/logger.py",
    "src/utils.py",
    "notebook/data/test.csv",
    "notebook/EDA.ipynb",
    "README.md",
    "requirements.txt",
    ".gitignore",
    "setup.py",
    "Dockerfile",
    "application.py",
    "templates/index.html",
    "static/css/styles.css",
    "static/images/"
]

def create_empty_file(filepath):
    with open(filepath, "w", encoding="utf-8", newline="\n"):
        pass

def create_directory_if_not_exists(directory):
    os.makedirs(directory, exist_ok=True)
    logging.info(f"Creating directory: {directory}")

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = filepath.parent, filepath.name

    if filedir:
        create_directory_if_not_exists(filedir)

    if not filepath.exists() or filepath.stat().st_size == 0:
        create_empty_file(filepath)
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

