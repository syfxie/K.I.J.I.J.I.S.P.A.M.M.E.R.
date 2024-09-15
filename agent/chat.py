import json
import cohere

import prompts
from utils import *


# Response format of the client
response_format = {
    "type": "json_object",
    "schema": {
        "type": "object",
        "required": ["casual", "rude", "lowball", "urgent"],
        "properties": {
            'casual': {"type": "string"},
            'rude': {"type": "string"},
            'lowball': {"type": "string"},
            'urgent': {"type": "string"}
        }
    }
}

class MessagingAgent:
    def __init__(self, system_msg=prompts.SYSTEM_MSG, product_description=prompts.PRODUCT_PROMPT_EXAMPLE) -> None:
        """
        Initialize the MessagingAgent with the provided system message and product description.
        
        Args:
            system_msg (str): The system message to be used in the chat history.
            product_description (str): The product description to be used in the chat history.
        """
        self.client = cohere.Client(API_KEY, log_warning_experimental_features=False)
        self.history = [
            {"role": "SYSTEM", "text": system_msg},
            {"role": "USER", "text": product_description}
        ]
    
    def gen_initial_msg(self) -> str:
        """
        Generate the initial message for each personality.
        
        Returns:
            dict: The dictionary of the initial message to send for each personality.
        """
        try:
            response = self.client.chat(
                message="Generate each personality's first message",
                chat_history=self.history,
                temperature=0.8,
                response_format=response_format
            )
            self.history = response.chat_history
            return json.loads(response.text)
        except Exception as e:
            print(f"Error generating initial message: {e}")
            return {}


    def gen_next_msg(self, msg_history: dict) -> str:
        """
        Generate the next message for each personality based on the provided message history.
        
        Args:
            msg_history (dict): Dictionary of message histories for each personality.
        
        Returns:
            dict: The dictionary of the next message to send for each personality.
            Ex: {
                "casual": "Hmm, let me think about that."
                "urgent": "",
                "lowball": "Sounds good, how about tomorrow".
            }
        """
        prompt = prompts.next_msg_prompt(msg_history)

        try:
            response = self.client.chat(
                message=prompt,
                chat_history=self.history,
                temperature=0.8,
                response_format=response_format
            )
            self.history = response.chat_history
            return json.loads(response.text)
        except Exception as e:
            print(f"Error generating next message: {e}")
            return {}


    def validate_response(response: str) -> bool:
        return True

if __name__ == '__main__':
    agent = MessagingAgent(prompts.SYSTEM_MSG)
    print(agent.gen_initial_msg())

    # Sample message histories for testing
    sample_msgs = {
        'casual': {
            'user': "Hi there! I'm interested in the item you have for sale. Could you tell me more about it?",
            'seller': "Of course! It's a high-quality item in excellent condition.",
            'user': "That sounds great. Can you tell me if there’s any flexibility on the price?",
            'seller': "I can offer a small discount if you’re interested."
        },
        'urgent': {
            'user': "I need this item urgently. Can you give me a final price quickly?",
            'seller': "I can give you a deal if you act fast.",
            'user': "I need to know the exact price now, or I’ll have to move on.",
            'seller': "I can reduce the price, but I need to finalize this quickly."
        },
        'rude': {
            'user': "Your price is outrageous. Do you even want to sell this item?",
            'seller': "I believe the price is fair for the quality.",
            'user': "Fair? It’s a joke. Drop the price if you want to make a sale.",
            'seller': "I’m already offering a good deal. Take it or leave it."
        },
        'lowball': {
            'user': "I’m only willing to pay half of your asking price. Let me know if you can accept it.",
            'seller': "That’s far too low. I can't sell it for that price.",
            'user': "I’m serious about my offer. If you can’t accept, I’ll look elsewhere.",
            'seller': "I appreciate your offer, but it’s too low for me to consider."
        }
    }

    response = agent.gen_next_msg(sample_msgs)
    print(response)
