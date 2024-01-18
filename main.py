import os
import streamlit as st
from memory_module import cast_memory, story_memory, story_object_memory
from chains_module import cast_chain, arc_chain, quest_chain, act_chain, objective_chain, story_chain, story_object_chain
from file_processing_module import write_to_file_in_folder
from globals import story_object_skeleton
from langchain.callbacks import StreamlitCallbackHandler

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# App Structure
st.title('Visual_Novel_StoryGen')
prompt = st.text_input(
    "Enter a story title")

# msgs = StreamlitChatMessageHistory()

# if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
#     msgs.clear()


# Response from the AI
if prompt:
    # response = sequential_chain({"title": prompt})
    cast = cast_chain.run(prompt)
    st.write(cast)
    write_to_file_in_folder(prompt,"cast",cast)
    arcs = arc_chain.run(cast=cast)
    # st.write(arcs)
    write_to_file_in_folder(prompt,"arcs",arcs)
    quests = quest_chain.run(arcs=arcs)
    # st.write(quests)
    write_to_file_in_folder(prompt,"quests",quests)
    acts = act_chain.run(quests=quests)
    # st.write(acts)
    write_to_file_in_folder(prompt,"acts",acts)
    story = story_chain.run(cast=cast, arcs=arcs,quests=quests, acts=acts)
    # st.write(story)
    write_to_file_in_folder(prompt,"story",story)
    objectives = objective_chain.run(acts=acts)
    write_to_file_in_folder(prompt,"objectives",objectives)
    story_object = story_object_chain.run(story=story, story_object_skeleton=story_object_skeleton, objectives=objectives)
    write_to_file_in_folder(prompt,"story_object",story_object)
    st.write(story_object)
    
    
    
    # avatars = {"human": "user", "ai": "assistant"}

    # History Chats
    with st.expander("Cast History"):
        st.info(cast_memory.buffer)

    # with st.expander("Story History"):
    #     st.info(story_memory.buffer)
    
    # with st.expander("Story Object History"):
        # st.info(story_object_memory.buffer)
        

# tools = load_tools(["ddg-search"])
# agent = initialize_agent(
#     tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
# )

# # Chat Interface

# if "messages" not in st.session_state:
#     st.session_state.messages = []
    
# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("Say something:"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         st_cb = StreamlitCallbackHandler(st.container())
#         response = 
#         full_response = ""

