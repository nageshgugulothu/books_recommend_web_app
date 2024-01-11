import os
import sys
import pandas as pd
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.utils import save_model
from src.components.data_ingestion import DataIngestion
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class DataTransformationConfig:
    book_list_obj_file = os.path.join('artifacts', 'book_list.pkl')
    similarity_obj_file = os.path.join('artifacts', 'similarity.pkl')

class DataTransformation:
    def __init__(self, df):
        self.data_transformation_config = DataTransformationConfig()
        self.df = df

    def initiate_data_transformation(self):
        try:
            logging.info('Data Transformation initiated')

            self.process_text_data()

            similarity = self.compute_cosine_similarity()

            # Example usage of recommend function
            recommended_books = self.recommend('Fundamentals of Wavelets')
            for book in recommended_books:
                print(book)

            # Save both model files
            save_model(
                self.data_transformation_config.book_list_obj_file,
                self.df,
                self.data_transformation_config.similarity_obj_file,
                similarity
            )

            logging.info('Pickle files saved')

            return (
                self.data_transformation_config.book_list_obj_file,
                self.data_transformation_config.similarity_obj_file
            )

        except Exception as e:
            logging.error("Exception occurred in data transformation")
            raise CustomException(e, sys)

    def process_text_data(self):
        cv = CountVectorizer(max_features=5000, stop_words="english")
        vectors = cv.fit_transform(self.df['tags'].astype(str)).toarray()
        ps = PorterStemmer()

        def stem(text):
            y = [ps.stem(i) for i in text.split()]
            return " ".join(y)

        self.df['tags'] = self.df['tags'].apply(stem)

    def compute_cosine_similarity(self):
        vectors = CountVectorizer().fit_transform(self.df['tags'].astype(str)).toarray()
        return cosine_similarity(vectors)

    def recommend(self, book):
        book_index = self.df[self.df['Title'] == book].index[0]
        distances = self.compute_cosine_similarity()[book_index]
        books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_books = [self.df.iloc[i[0]]['Title'] for i in books_list]
        return recommended_books

if __name__ == '__main__':
    obj = DataIngestion()
    raw_data_path, books_data_path = obj.initiate_data_ingestion()
    df = pd.read_csv(books_data_path)  # Read the books data
    data_transformation = DataTransformation(df)
    data_transformation.initiate_data_transformation()
