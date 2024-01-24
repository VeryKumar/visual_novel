from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class ObjectiveEvaluator:
    def __init__(self, llm):
        self.llm = llm or ChatOpenAI(
            model='gpt-4-1106-preview',
            streaming = True,
        )
        #V1
        # prompt = ChatPromptTemplate.from_template("""Act Progress Checker:
        # ---------
        # Current Act Objective: {detailed_objective}
        # Last Messages: {last_messages}
        # ---------
        # Evaluate if the objective is met, partially met, or not met. Respond with one of these three options + explaination.
        # Completion Status:
        # Explaination:""")
        
        #V2
        prompt = ChatPromptTemplate.from_template("""Act Progress Checker:
        ---------
        Current Act Objective: {detailed_objective}
        Last Messages: {last_messages}
        ---------
        Evaluate if the objective is met, partially met, or not met. Respond with a number from 0-100, with 1 being not met at all and 100 being completely met.
        Completion Status:""")

        
        self.chain = LLMChain(llm=self.llm, prompt=prompt, verbose=True, output_key='completion_status')