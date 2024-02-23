import os
import sys
import pandas as pd
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_model
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def train_model_logic(self, df):

        tags = df['tags']
        print(df.head(3))

        # Vectorize the 'tags' using CountVectorizer
        cv = CountVectorizer(max_features=5000, stop_words="english")
        vectors = cv.fit_transform(tags.astype(str)).toarray()

        # Compute cosine similarity between items (books)
        similarity_matrix = cosine_similarity(vectors)

        # Save the similarity matrix
        save_model('artifacts/similarity.pkl', similarity_matrix)

        return similarity_matrix

    def train_model(self):
        try:
            # Data Ingestion
            data_ingestion = DataIngestion()
            _, books_data_path = data_ingestion.initiate_data_ingestion()

            # Data Transformation
            df = pd.read_csv(books_data_path)

            # Train your model
            similarity_matrix = self.train_model_logic(df)

            # Save the similarity matrix
            save_model('artifacts/similarity.pkl', similarity_matrix)

            logging.info("Model training completed.")

        except Exception as e:
            logging.error("Exception occurred in data transformation")
            raise CustomException(e, sys)

if __name__ == '__main__':
    obj = DataIngestion()
    raw_data_path, books_data_path = obj.initiate_data_ingestion()
    df = pd.read_csv(books_data_path)  # Read the books data
    data_transformation = DataTransformation(df)
    data_transformation.initiate_data_transformation()
    model_trainer = ModelTrainer()
    model_trainer.train_model()
