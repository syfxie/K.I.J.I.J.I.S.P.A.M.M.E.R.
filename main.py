import pandas as pd
import time

from orchestrator import Orchestrator
from agent import MessagingAgent, FilteringAgent, DealClosingAgent


if __name__ == "__main__":
    orchestrator = Orchestrator(count=2)
    agent_names = orchestrator.get_agent_names()
    # negotiator = DealClosingAgent()

    # Dict : DataFrame
    inital_convos = orchestrator.get_data()
    while True:
        is_update = orchestrator.check_for_update()
        if is_update: 
            print("THERE IS AN UPDATE -----")
            agents_to_respond, messages = orchestrator.get_data()
            print("New messages: ", messages)
            print(f"Most Recent Agent: {agents_to_respond}")

            agent = MessagingAgent()
            next_messages = agent.gen_next_msg(messages, agents_to_respond)
            print("Agent responses: ", next_messages)

        time.sleep(10)



    time.sleep(10)
    orchestrator.close()

