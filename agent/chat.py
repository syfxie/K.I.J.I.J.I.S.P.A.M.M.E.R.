import json
import cohere

import agent.prompts as prompts
from agent.utils import *


# Response format of the LLM
response_format = {
    "type": "json_object",
    "schema": {
        "type": "object",
        "required": ["Agent 1", "Agent 2"],
        "properties": {
            'Agent 1': {"type": "string"},
            'Agent 2': {"type": "string"},
        }
    }
}

class MessagingAgent:
    def __init__(self, system_msg=prompts.MSG_AGENT_SYSTEM_MSG, target_price=800, product_description=prompts.PRODUCT_DESCRIOTION_EXAMPLE) -> None:
        """
        Initialize the MessagingAgent with the provided system message and product description.
        
        Args:
            system_msg (str): The system message to be used in the chat history.
            target_price (int): The maximum price that the user is willing to pay.
            product_description (str): The product description to be used in the chat history.
        """
        
        self.client = cohere.Client(API_KEY, log_warning_experimental_features=False)
        self.history = [
            {"role": "SYSTEM", "text": system_msg  + f" \nYour target price: {target_price}"},
            {"role": "USER", "text": product_description}
        ]
        self.target_price = target_price
    
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


    def gen_next_msg(self, msg_history: dict, agents_to_update: list) -> str:
        """
        Generate the next message for each personality based on the provided message history.
        
        Args:
            msg_history (dict): Dictionary of all the message histories for each personality.
        
        Returns:
            dict: The dictionary of the next message to send for each personality.
            Ex: {
                "Agent 1": "Hmm, let me think about that."
                "Agent 2": "",
            }
        """
        prompt = prompts.next_msg_prompt(msg_history)
        prompt += f" \n\nTarget price: {self.target_price}. Do not offer prices above this target."

        try:
            response = self.client.chat(
                message=prompt,
                chat_history=self.history,
                temperature=0.8,
                response_format=response_format
            )
            self.history = response.chat_history
            response_json = json.loads(response.text)

            # Only generate new responses for agents that received messages from the seller
            for key in response_json.keys():
                if not key in agents_to_update:
                    response_json[key] = ""

            # Return the messages as a JSON
            return response_json
        except Exception as e:
            print(f"Error generating next message: {e}")
            return {}
        

if __name__ == '__main__':
    agent = MessagingAgent(prompts.MSG_AGENT_SYSTEM_MSG)
    print(agent.gen_initial_msg())

    # Sample message histories for testing
    sample_msgs = {
        'casual': {
            'user': "Hi there! I'm interested in the item you have for sale. Could you tell me more about it?",
            'seller': "Of course! It's a high-quality item in excellent condition.",
            'user': "That sounds great. Can you tell me if there’s any flexibility on the price?",
            'seller': "I can offer a small discount if you’re interested."
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
