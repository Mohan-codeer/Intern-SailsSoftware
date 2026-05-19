from langchain_groq import *
from langchain import *
from langchain_core.messages import *
from dotenv import load_dotenv
from constant.constants import planning_system_prompt, research_system_prompt, reasoning_system_prompt, critic_system_prompt, final_system_prompt
from classes.agent import Agent 
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    api_key=api_key,
    model="llama-3.1-8b-instant"
)

user_input = input("User: ")

planner_agent = Agent("Planner Agent", planning_system_prompt, llm)
research_agent = Agent("Reasearch Agent", research_system_prompt, llm)
reasoning_agent = Agent("Reasoning Agent", reasoning_system_prompt, llm)
critic_agent = Agent("Critic Agent", critic_system_prompt, llm)
final_agent = Agent("Final Agent", final_system_prompt, llm)

planner_response = planner_agent.run(user_input)
research_response = research_agent.run(user_input + planner_response)
reasoning_response = reasoning_agent.run(user_input + planner_response + research_response)
critic_response = critic_agent.run(user_input + planner_response + research_response + reasoning_response)
final_response = final_agent.run(user_input + planner_response + research_response + reasoning_response + critic_response)

print(f"Planner: {planner_response}")
print(f"Researcher: {research_response}")
print(f"Reasoner: {reasoning_response}")
print(f"Critic: {critic_response}")
print(f"Final: {final_response}")
