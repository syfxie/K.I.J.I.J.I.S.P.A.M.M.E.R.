import os
import cohere
from dotenv import load_dotenv

import bargain_prompts
from utils import *

load_dotenv()
API_KEY = os.getenv("COHERE_API_KEY")

class BargainAgent():
    def __init__(self, system_msg=bargain_prompts.SYSTEM_MSG, product_description=bargain_prompts.PRODUCT_PROMPT_EXAMPLE) -> None:
        self.client = cohere.Client(API_KEY, log_warning_experimental_features=False)
        self.history=[
            {"role": "SYSTEM", "text": system_msg},
            {"role": "USER", "text": product_description},
        ]
    
    def gen_initial_msg(self):
        try:
            response = self.client.chat(
                message="Generate each personality's first message",
                chat_history=self.history,
                temperature=0.8,
                response_format={
                    "type": "json_object",
                    "schema": {
                        "type": "object",
                        "required": PERSONALITIES,
                        "properties": {
                            'casual': { "type": "string"},
                            'rude': { "type" : "string"},
                            'lowball': { "type" : "string"},
                            'urgent': { "type" : "string"}
                        }
                    }
                },
            )
            self.history = response.chat_history
            return response.text
        except Exception as e:
            print(e)
    
    def validate_response(response):
        pass

if __name__ == '__main__':
    agent = BargainAgent(SYSTEM_MSG)
    print(co.gen_initial_msg())