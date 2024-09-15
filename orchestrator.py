import os
import pandas as pd
from dotenv import load_dotenv
from WebAgent import WebAgent

load_dotenv()

ACCOUNTS = [
    {
        "username": os.environ.get("HELIOS_KIJIJI_USERNAME"),
        "password": os.environ.get("HELIOS_KIJIJI_PASSWORD"),
    },
    {
        "username": os.environ.get("AJ_KIJIJI_USERNAME"),
        "password": os.environ.get("AJ_KIJIJI_PASSWORD"),
    },
]


class Orchestrator:
    def __init__(self, count=1):
        self.count = count
        # Returns a list of dataframes to get full converstation history
        self.web_agents = [WebAgent() for i in range(count)]
        # Each web agent will add to a different dataframe
        self.dfs = {
            w: pd.DataFrame(columns=["direction", "text"]) for w in self.web_agents
        }

        self.agents_with_message = []

        for i in range(count):
            self.web_agents[i].set_name(f"Agent {i + 1}")
            self.web_agents[i].set_username(ACCOUNTS[i]["username"])
            self.web_agents[i].set_password(ACCOUNTS[i]["password"])
            self.web_agents[i].login_kijiji()
            self.web_agents[i].goto_first_convo()
            self.dfs[self.web_agents[i]] = self.web_agents[i]._parse_convo()

    def get_agent_names(self):
        return [agent.name for agent in self.web_agents]

    def check_for_update(self):
        is_update = False
        self.agents_with_message = []
        for agent in self.web_agents:
            new_df = agent._parse_convo()
            if (
                self.dfs[agent]["direction"].str.contains("seller").sum()
                < new_df["direction"].str.contains("seller").sum()
            ):
                self.dfs[agent] = new_df
                self.agents_with_message.append(agent.name)
                print(f"Agent {agent.name} has a new message!")
                is_update = True

        return is_update

    def get_data(self):
        res = {}
        for agent in self.web_agents:
            res[agent.name] = [tuple(row) for row in self.dfs[agent].values]

        return (self.agents_with_message, res)

    def send_message(self, agent_name: str, message: str) -> None:
        print("agent_name: ", agent_name)
        i = int(agent_name.split(" ")[1]) - 1  # parses agent index from name
        self.web_agents[i].send_message(message)

    def get_agent_info(self, agent_name: str) -> tuple:
        i = int(agent_name.split(" ")[1]) - 1
        return (self.web_agents[i].username, self.web_agents[i].password)

    def close(self):
        for agent in self.web_agents:
            agent.close()
