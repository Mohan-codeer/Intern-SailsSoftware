from langchain_core.messages import *

class Agent:

    def __init__(self, name, system_prompt, llm):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm

    def run(self, input_text):
        response = self.llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input_text)
        ])
        return response.content
