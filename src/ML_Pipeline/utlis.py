import json
import pandas as pd
from ML_Pipeline.db import UserQuery, IntentFlow

client_id = 88


# Function to read the data file
def read_data(file_path, **kwargs):
    raw_data = pd.read_json(file_path, **kwargs)
    return raw_data


# Function to get "not answered question from user by chatbot"
def get_client_query():
    cursor_list = UserQuery(client_id)
    query_list = cursor_list.get_query()
    queries = []
    for obj in query_list:
        queries.append(obj['query'])
    return queries


def regrex_code(text):
    return text.strip().replace('\"', '').replace('\'', '').replace('?', '').replace(',', '').replace('!', '') \
        .replace('“', "").replace('”', "").lower()
