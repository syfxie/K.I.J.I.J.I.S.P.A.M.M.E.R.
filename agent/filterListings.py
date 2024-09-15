
import ast
import json 
import pandas as pd
import cohere

from chat import MessagingAgent


SYSTEM_MSG = """
    Your are a product recommendation assistant. Find the top 5 most relevant and credible listings based on the user query, and return their URL's.
    If there are less than 5 listings given, return all.

    Given:
    - user_query (str): The product the user is looking for.
    - listings (list of dicts): A list where each dict contains:
        - 'Title': The name of the product.
        - 'Description': A brief description of the product.
        - 'Price': The price of the product.
        - 'URL': The link to the product.

    Returns:
    - list of str: A list of the top 5 URLs that best match the user query.
"""

listings_excel_path = "agent/data.xlsx"
dest_excel_path = "agent/initial_msgs.xlsx"


class FilteringAgent():
    def __init__(self, system_msg=SYSTEM_MSG) -> None:
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
            for url in url_list:
                agent = MessagingAgent()
                messages_json[url] = agent.gen_initial_msg()
            
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
    agent = FilteringAgent(SYSTEM_MSG)
    print(agent.get_recommendations("I want a ThinkPad", listings_path=listings_excel_path))
