import os
import pandas as pd
from dotenv import load_dotenv
from WebAgent import WebAgent

load_dotenv()

ACCOUNTS = [
    {"username": os.environ.get("HELIOS_KIJIJI_USERNAME"), "password": os.environ.get("HELIOS_KIJIJI_PASSWORD")},
    {"username": os.environ.get("AJ_KIJIJI_USERNAME"), "password": os.environ.get("AJ_KIJIJI_PASSWORD")},
]


class Orchestrator:
    def __init__(self, count=2):
        # Returns a list of dataframes to get full converstation history
        self.web_agents = [WebAgent() for i in range(count)]
        # Each web agent will add to a different dataframe
        self.dfs = {
            w: pd.DataFrame(columns=["direction", "text"]) for w in self.web_agents
        }

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
        for agent in self.web_agents:
            new_df = agent._parse_convo()
            if len(self.dfs[agent]) < len(new_df):
                self.dfs[agent] = new_df
                print(f"Agent {agent.name} has a new message!")
                return True
        
        return False

    def get_data(self):
        res = {}
        for agent in self.web_agents:
            res[agent.name] = [tuple(row) for row in self.dfs[agent].values]
        
        return res

    def close(self):
        for agent in self.web_agents:
            agent.close()
            3