import os
import streamlit as st
from memory_module import cast_memory, story_memory
from chains_module import cast_chain, arc_chain, quest_chain, act_chain, story_chain

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# App Structure
st.title('Visual_Novel_StoryGen')
prompt = st.text_input(
    "Enter a story title")

# Response from the AI
if prompt:
    # response = sequential_chain({"title": prompt})
    cast = cast_chain.run(prompt)
    arcs = arc_chain.run(cast=cast)
    quests = quest_chain.run(arcs=arcs)
    acts = act_chain.run(quests=quests)
    story = story_chain.run(cast=cast, arcs=arcs,quests=quests, acts=acts)

    st.write(cast)
    st.write(arcs)
    st.write(quests)
    st.write(acts)
    st.write(story)

    # History Chats
    with st.expander("Cast History"):
        st.info(cast_memory.buffer)

    with st.expander("Story History"):
        st.info(story_memory.buffer)