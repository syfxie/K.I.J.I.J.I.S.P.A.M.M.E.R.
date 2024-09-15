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
  "casual": casual buyer's next message,
  "rude": rude buyer's next message,
  "lowball": lowball buyer's next message,
  "urgent": urgent buyer's next message
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


def product_prompt(title, description, price, target_price):
    prompt = f"""
This is the product you want to purchase:
Name: {title}
Description: {description},
Listed price: {price},

You want to coordinate negotations with your different personalities to reach a price of: {target_price}.
"""
    return prompt


def next_msg_prompt(msgs):
    """
    Generates the next message to send for each of the personalities that received a response from the seller. 
    If no response/if the latest message was sent by the user and not the seller, then return an empty string for that personality.

    Return: a JSON with the next message for each user.
        {
            "casual": casual buyer's next message,
            "rude": rude buyer's next message,
            "lowball": lowball buyer's next message,
            "urgent": urgent buyer's next message
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
    prompt = f"""
Below are the negotiation histories for four different personalities:

{msgs}

Determine the next message for each personality. If the user's message was the last one in the conversation, return an empty string for that personality.

Your goal is to negotiate the best price. Adapt each personality's strategy accordingly and coordinate the personalities to work together.
"""
    return prompt
