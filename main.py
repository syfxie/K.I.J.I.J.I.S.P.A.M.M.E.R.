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
            messages = orchestrator.get_data()
            print(messages)
            agent = MessagingAgent()
            next_messages = agent.gen_next_msg(messages)
            print(next_messages)

        time.sleep(10)



    time.sleep(10)
    orchestrator.close()

