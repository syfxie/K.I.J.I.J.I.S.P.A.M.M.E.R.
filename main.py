import pandas as pd
import time

from orchestrator import Orchestrator
from agent import MessagingAgent, FilteringAgent, DealClosingAgent
from gui import GUI



if __name__ == "__main__":
    print("start gui")
    gui = GUI()
    print("end gui")
    
    print('main looping')
    gui.root.mainloop()
    print('done main loop')
    
    # gui.root.wait_variable(gui.can_retrieve_input)
    # print('done waiting')

    # Run computations using the selected value
    selected_value = gui.can_retrieve_input.get()

    print("input received from gui")
    input_data = gui.retrieve_input()
    max_price = input_data["max_price"]
    print("input data received: ", input_data)
    
    orchestrator = Orchestrator(count=1)
    agent_names = orchestrator.get_agent_names()
    # negotiator = DealClosingAgent()

    # Dict : DataFrame
    inital_convos = orchestrator.get_data()
    WINNING_AGENT_NAME = None
    WINNER_FOUND = False
    message_agent = MessagingAgent(target_price=max_price)
    closing_agent = DealClosingAgent()
    while not WINNER_FOUND:
        is_update = orchestrator.check_for_update()
        if is_update: 
            print("THERE IS AN UPDATE -----")
            agents_to_respond, messages = orchestrator.get_data()
            print("New messages: ", messages)
            print(f"Most Recent Agent: {agents_to_respond}")

            for name in orchestrator.get_agent_names():
                msg = messages[name]
                print("!!!checking win condition!!!")
                print(name)
                print(msg)
                if closing_agent.check_deal_status(msg):
                    WINNING_AGENT_NAME = name
                    WINNER_FOUND = True
                    break
            if WINNER_FOUND: break

            next_messages = message_agent.gen_next_msg(messages, agents_to_respond)
            if len(agents_to_respond) > 0:
                for agent in agents_to_respond:
                    orchestrator.send_message(agent, next_messages[agent])

            print("Agent responses: ", next_messages)

        time.sleep(2)

    orchestrator.close()

    print(WINNING_AGENT_NAME)
    WINNING_USER, WINNING_PASS = orchestrator.get_agent_info(WINNING_AGENT_NAME) 
    gui.display_success(WINNING_USER, WINNING_PASS)

    time.sleep(10)

    input("press enter to close...")

