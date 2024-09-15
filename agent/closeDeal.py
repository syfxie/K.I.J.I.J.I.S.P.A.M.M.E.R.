import json
import cohere

from agent.prompts import CLOSE_DEAL_SYSTEM_MSG
from agent.utils import *


class DealClosingAgent:
    def __init__(self, system_msg=CLOSE_DEAL_SYSTEM_MSG) -> None:
        """
        Initialize the DealClosingAgent with the provided system message.
        
        Args:
            system_msg (str): The system message to be used in the chat history.
        """
        self.client = cohere.Client(API_KEY, log_warning_experimental_features=False)
        self.history = [{"role": "SYSTEM", "text": system_msg}]
    
    def check_deal_status(self, msgs):
        """
        Given the message history of one conversation, determines if a deal has been reached.
        
        Args:
            msgs: List of messages with sender and message content.
        
        Returns:
            bool: True if a deal has been closed, otherwise False.
        """

        try:
            response = self.client.chat(
                message=f"Below is the message history: {msgs}",
                chat_history=self.history,
                temperature=0.1,
                response_format={
                    "type": "json_object",
                    "schema": {
                        "type": "object",
                        "required": ['status'],
                        "properties": {
                            'status': {"type": "string", "enum": ["True", "False"]}
                        }
                    }
                }
            )
            # Parse and interpret the response
            result = json.loads(response.text)
            if result.get('status') == "True":
                print("Deal has been closed!")
                return True
            else:
                return False
        except Exception as e:
            print(f"Error checking deal status: {e}")
            return False

if __name__ == '__main__':
    # Sample message for testing
    sample_msg = [
        {"sender": "Buyer", "message": "Hey, I'm looking to buy 10 of your wireless headphones. What's the best price you can give me for that?"},
        {"sender": "Seller", "message": "Hi! Thanks for asking. If you're getting 10, I can do $45 per unit, down from the usual $50. Plus, shipping's on us."},
        {"sender": "Buyer", "message": "$45 is still a bit high for me. Any chance you could go down to $40 if I order today?"},
        {"sender": "Seller", "message": "I get it. How about we meet in the middle at $42? That's the best I can do for an order of 10."},
        {"sender": "Buyer", "message": "$42 sounds fair. Let's go ahead with that."},
        {"sender": "Seller", "message": "Great! I'll send over an invoice for $420. Once you pay, we'll get everything ready to go."},
        {"sender": "Buyer", "message": "Awesome, I'll pay right now. Thanks!"},
        {"sender": "Seller", "message": "Thanks so much! I'll keep an eye out for the payment."}
    ]
    
    agent = DealClosingAgent(CLOSE_DEAL_SYSTEM_MSG)
    print(agent.check_deal_status(sample_msg))
