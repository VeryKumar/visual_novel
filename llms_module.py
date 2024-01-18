# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from callbacks import StreamHandler
import streamlit as st

stream_handler = StreamHandler(st.empty())


llm = ChatOpenAI(
            model='gpt-4-1106-preview',
            streaming = True,
            callbacks=[stream_handler]
            
)

jsonModeModel = ChatOpenAI(model = "gpt-4-1106-preview", model_kwargs={"response_format": {"type": "json_object"}})