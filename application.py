from flask import Flask, render_template, request
import pandas as pd
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

app = Flask(__name__)

@app.route('/')
def index():
    # Read the DataFrame from a CSV file (adjust the file path accordingly)
    df = pd.read_csv('artifacts/books_data.csv')
    
    # Get a list of unique book titles
    book_titles = df['Title'].unique().tolist()

    return render_template('index.html', book_titles=book_titles)

@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form['book_title']

    # Read the DataFrame from a CSV file (adjust the file path accordingly)
    df = pd.read_csv('artifacts/books_data.csv')

    # Data Ingestion
    data_transformation = DataTransformation(df)
    data_transformation.initiate_data_transformation()

    # Model Training
    model_trainer = ModelTrainer()
    model_trainer.train_model()

    # Recommendation Logic
    recommended_books = data_transformation.recommend(book_title)

    return render_template('result.html', book_title=book_title, recommended_books=recommended_books)

if __name__ == '__main__':
    app.run(debug=True)
