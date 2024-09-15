import ast
import json 
import pandas as pd
import cohere

from agent.chat import MessagingAgent
from agent.prompts import FILTER_SYSTEM_MSG
from agent.utils import *

listings_excel_path = "data.xlsx"
dest_excel_path = "initial_msgs.xlsx"


class FilteringAgent():
    def __init__(self, system_msg=FILTER_SYSTEM_MSG) -> None:
        self.client = cohere.Client(API_KEY, log_warning_experimental_features=False)
        self.history=[
            {"role": "SYSTEM", "text": system_msg}
        ]
    
    def get_recommendations(self, user_query, listings_path):
        # Read the spreadsheet of listings as a JSON 
        listings_json = excel_to_json(listings_path)
        prompt = f"""
User query: {user_query}
Listings: {listings_json}

Return the URL's of the top 5 recommendations as a list.
"""
        try:
            response = self.client.chat(
                message=prompt,
                chat_history=self.history,
                temperature=0.8,
            )
            self.validate_response(response)
            self.history = response.chat_history
            url_list  = str_to_list(response.text)

            messages_json = {}

            # Generate an initial message for each of the recommended products
            for url in url_list:
                agent = MessagingAgent()
                messages_json[url] = agent.gen_initial_msg()
            
            # Save the messages to an excel
            json_to_excel(messages_json, dest_excel_path)
            return messages_json

        except Exception as e:
            print("Error: ", e)
    
    def validate_response(self, response):
        if not response.text:
            print("Invalid filtering response")
            print(response)
            return
        return ast.literal_eval(response.text)


def excel_to_json(excel_file_path, sheet_name=0):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    json_data = df.to_dict(orient='records')
    return json_data


def json_to_excel(json_data, excel_filename):
    if isinstance(json_data, str):
        data = json.loads(json_data)  # Parse string if it is JSON string
    else:
        data = json_data  # If it's already a Python dictionary or list
    df = pd.json_normalize(data)
    df.to_excel(excel_filename, index=False, engine='openpyxl')


def str_to_list(s):
    s = s.strip("[]")
    s = s.split(", ")
    s = [item.strip("'") for item in s]
    print(s)
    return s


if __name__ == '__main__':
    agent = FilteringAgent(FILTER_SYSTEM_MSG)
    print(agent.get_recommendations("I want a ThinkPad", listings_path=listings_excel_path))
