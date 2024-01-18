from pymongo import MongoClient
import json
import csv
import pandas as pd


def csv_to_json(csv_file_path, json_file_path):
    # Read CSV file
    with open(csv_file_path, 'r') as csv_file:
        csv_data = csv.DictReader(csv_file)
        # Convert CSV data to a list of dictionaries
        data = [row for row in csv_data]

    # Write JSON data to file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Provide the file paths
csv_file_path = r"C:/Users/sbc/Downloads/books_data.csv"
json_file_path = r"C:/Users/sbc/Downloads/books_data.json"

# Convert CSV to JSON
csv_to_json(csv_file_path, json_file_path)

# Set up connection details:
connection_string = "mongodb+srv://nageshgugulothu:kushal@cluster0.edjtkdn.mongodb.net/?retryWrites=true&w=majority"

# connection_string = "mongodb+srv://nageshgugulothu:abcdef@cluster0.edjtkdn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

db = client['nageshdb']
collection = db['books_data']

# Load JSON data
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)


# Insert data into MongoDB
collection.insert_many(data)