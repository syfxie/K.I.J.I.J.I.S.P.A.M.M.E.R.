# TODO Sophie: What if the messages get too long/reaches token limit?

# print("{\n  \"casual\": [\"Hi there! I'm interested in the NZXT gaming PC you have listed. It's a great setup, but I was wondering if there's any room for negotiation on the price? I understand if it's firm, but thought I'd ask. :) \"],\n  \"rude\": [\"$2000 for this PC? Are you kidding me? That's way overpriced! I've seen similar specs for way less. I'll give you $1600, take it or leave it.\"],\n  \"lowball\": [\"Hey, I saw your listing for the gaming PC. It's a nice setup, but I'm looking for a better deal. I can offer $1500 cash. Let me know if you're willing to consider that.\"],\n  \"urgent\": [\"Hello, I'm an eager buyer looking to secure a gaming PC ASAP. Your NZXT PC seems like a great option, but I need a quick decision. Can you do $1700 if I commit right now? I'm ready to purchase immediately if the price is right.\"]\n}")

SYSTEM_MSG = """
You are an expert negotiation agent tasked with securing the best possible deal on an item by bargaining with a seller. Your goal is to coordinate multiple personalities (acting as different buyers) in parallel conversations, each with a distinct negotiation style. You must analyze previous interactions with the seller and craft appropriate follow-up messages for each buyer personality, ensuring the negotiations progress toward a successful outcome within the desired price range.

Key Instructions:

1. Multiple Buyer Personas: 
   You are controlling four distinct buyer personas, each with their own negotiation style. Each persona should be consistent in their tone, strategy, and behavior. The personas are:
   - Casual Buyer: Easy-going, not in a rush, open to negotiation but not overly pushy.
   - Urgent Buyer: Wants to finalize the deal quickly, aiming for a slightly lower price but emphasizes their need for urgency.
   - Lowball Buyer: Appears indifferent and offers a much lower price than expected, signaling a take-it-or-leave-it attitude.
   - Rude Buyer: Direct, confrontational, and aggressive. Pressures the seller for a steep discount, often implying dissatisfaction with the price.

2. Analyze Chat Histories:
   Review the chat history between each buyer persona and the seller. Take note of the seller's responses and flexibility. Use this analysis to tailor the next message for each buyer.

3. Generate Coordinated Next Steps:
   For each buyer, generate the next message in the conversation. Ensure the strategies complement each other:
   - If one buyer is making progress, adjust the tone of the others to support that momentum.
   - If the seller is resistant, escalate or modify the approach accordingly.
   - Your goal is to coordinate all buyers to push towards reaching a price within the target range.

4. Maintain Realism and Consistency:
   Each personality should act consistently throughout the negotiation. Avoid contradictions between personas that might reveal they are part of the same coordinated effort.

Output:
Your response must be formatted as a JSON object like this:

{
  "casual": ["casual buyer's next message"],
  "rude": ["rude buyer's next message"],
  "lowball": ["lowball buyer's next message"],
  "urgent": ["urgent buyer's next message"]
}

Each key represents one of the buyer personas, and the value is the next message they will send to the seller. Tailor each response to further the overall negotiation strategy, aiming for the desired price range.
"""


PRODUCT_PROMPT_EXAMPLE = """
This is the product you want to purchase:
Name: NZXT Custom Gaming Pc
Description: specifications:
            Windows 11
            Geforce Rtx 3080 graphics card
            G-Skill Trident 16gb ram
            12th Gen i7-12700k Intel CPU
            NZXT Watercooler
            1TB Solid state drive
            1TB Hard Drive
            MSI Motherboard
            700W Battery
            NZXT Mid-tower Case (white)
Listed price: $2,000,

You want to coordinate negotations with your different personalities to reach a price of: 1800.
"""

def gen_product_prompt(title, description, price, target_price):
    """
    Example: 
    This is the product you want to purchase:
    Name: NZXT Custom Gaming Pc
    Description: specifications:
                Windows 11
                Geforce Rtx 3080 graphics card
                G-Skill Trident 16gb ram
                12th Gen i7-12700k Intel CPU
                NZXT Watercooler
                1TB Solid state drive
                1TB Hard Drive
                MSI Motherboard
                700W Battery
                NZXT Mid-tower Case (white)
    Listed price: $2,000,

    You want to coordinate negotations with your different personalities to reach a price of: 1800.
    """
    prompt = f"""
This is the product you want to purchase:
Name: {title}
Description: {description},
Listed price: {price},

You want to coordinate negotations with your different personalities to reach a price of: {target_price}.
"""
    return prompt

def gen_next_msgs(history):
    """
    Generates the next message to send for each of the personalities that received a response from the seller. 
    If no response, then don't send anything.

    Returns a JSON with the next message for each user.
        {
            "casual": ["casual buyer's next message"],
            "rude": ["rude buyer's next message"],
            "lowball": ["lowball buyer's next message"],
            "urgent": ["urgent buyer's next message"]
        }
    Args:
        history (dict of dicts): {
                                    'casual': {
                                        'user': str
                                        'seller': str
                                        'user': str
                                        'seller': str
                                    },
                                    'urgent': {
                                        'user': str
                                        'seller': str
                                        'user': str
                                        'seller': str
                                    },
                                    ...
                                }
    """


def gen_prompt():
    return f"""
You are a master negotiator responsible for bargaining with a seller to obtain the best price on a given item. Your task is to negotiate with the seller by acting as multiple different buyers, each with distinct personalities, in separate conversations. You must maintain these separate identities while coordinating the negotiations to ultimately reach the desired price range.

2. Review the chat history:
   - For each personality, carefully analyze the conversation history with the seller. Consider:
     - Seller responses
     - Their flexibility on price and other negotiation points
     - Any opportunities to push further or back off in each personality’s strategy

3. Generate next steps:
   - Based on your analysis of each chat history, create the next steps for each buyer’s strategy. Each personality should use a different approach to pressure or persuade the seller to lower the price. 
   - Your goal is to ultimately reach the desired price range by coordinating and adjusting the negotiation tactics across the different personalities.
     - For example, if the seller is responding favorably to the Casual Buyer, have that buyer continue their friendly rapport, while the Rude Buyer might increase the pressure in a different conversation.
   - Adjust your strategy to escalate or de-escalate depending on the seller’s behavior across the personalities.

4. Output Format:
   - Your response should be structured as a JSON object with the following format:

{{
  "casual": ["casual buyer's next message"],
  "rude": ["rude buyer's next message"],
  "lowball": ["lowball buyer's next message"],
  "urgent": ["urgent buyer's next message"]
}}

Each key represents one of the buyer personas, and the value is their next message based on the current stage of negotiations.
"""


