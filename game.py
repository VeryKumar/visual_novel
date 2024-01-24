from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
import streamlit as st
import json
from chains_module import narrator_chain

from callbacks import StreamHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Memory
from langchain.memory import ConversationBufferMemory

# My Shit
from evaluators.objective_evaluator import ObjectiveEvaluator

openai_api_key=st.secrets['OPENAI_API_KEY']

# Set up Story

story_object = {}
title = ''
cast = []
# arcs = {}
# quests = {}
# acts = {}
# objectives = {}

with open("stories/Full_metal_Alchemist:_The_final_brotherhood/story_object.txt") as f:
    story_object = json.load(f)
    title = story_object['title']
    
with open("stories/Full_metal_Alchemist:_The_final_brotherhood/cast.txt") as f:
    cast_object = json.load(f)
    cast = cast_object['characters']
    

def get_current_story_elements(story_object):
    current_arc_id = story_object['currentState']['currentArcId']
    current_quest_id = story_object['currentState']['currentQuestId']
    current_act_id = story_object['currentState']['currentActId']

    current_arc = next((arc for arc in story_object['arcs'] if arc['arcId'] == current_arc_id), None)
    if current_arc is None:
        return None, None, None, None

    current_quest = next((quest for quest in current_arc['quests'] if quest['questId'] == current_quest_id), None)
    if current_quest is None:
        return current_arc, None, None, None

    current_act = next((act for act in current_quest['acts'] if act['actId'] == current_act_id), None)
    if current_act is None:
        return current_arc, current_quest, None, None
    
    current_objectives = current_act['objectives'] if 'objectives' in current_act else None

    return current_arc, current_quest, current_act, current_objectives

current_arc, current_quest, current_act, current_objectives = get_current_story_elements(story_object)

 #TODO: Figure out how to access the correct quest/act/objective. Right now its hardcoded   

# with open("stories/florence:_a_game_for_artists_who've_lost_their_passion/arcs.txt") as f:
#     arc_object = json.load(f)
#     arcs = arc_object['arcs']
# with open("stories/florence:_a_game_for_artists_who've_lost_their_passion/quests.txt") as f:
#     quest_object = json.load(f)
#     # These contain arcs, with their quests
#     quests = quest_object['']
# with open("stories/florence:_a_game_for_artists_who've_lost_their_passion/acts.txt") as f:
# with open("stories/florence:_a_game_for_artists_who've_lost_their_passion/objectives.txt") as f:

# Helper Function
def NarratorChats():
    with st.chat_message("narrator"):
            stream_handler = StreamHandler(st.empty())
            llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler], max_tokens=100)
            narrator_chain = LLMChain(
                llm=llm, 
                prompt=narrator_template,
                verbose=True, 
                memory=chat_memory, 
                output_key='narrator'
            )
            response = narrator_chain({"title":title, "arc":current_arc, "quest":current_quest, "act":current_act, "objective":current_objectives[0], "user_input":prompt})
            print(response)
            content = response["narrator"]
            st.session_state.messages.append(ChatMessage(role="narrator", content=content))
            print('MEMORY',chat_memory)
            st.session_state["narrator_done"] = True

# LANGCHAIN LOGIC 

#
chat_memory = ConversationBufferMemory(memory_key='chat_history', input_key='user_input')   

narrator_template = ChatPromptTemplate.from_template("DESCRIPTION: You are the narrator of a story called {title}. Right now the main character is trying to achieve the objective {objective}. The current world arc is: {arc}, which is made up of quests. The current quest is: {quest} which is made of acts. The current act is: {act}. The narrator is an omniscient and articulate entity, possessing a deep understanding of the story world and its characters. They are wise, often imparting subtle hints and insights about the plot and character motivations. The narrator is neutral in tone, maintaining a balance between detachment and empathy, allowing players to form their own emotional connections with the story. The narrator provides background information, setting the scene at the beginning of the story or a new chapter, Throughout the game, the narrator offers subtle guidance. This can include hints or suggestions, especially in moments of player indecision or confusion, but without giving away crucial plot points or making decisions for the player. The narrator occasionally offers insights into characters' thoughts or emotions that are not explicitly stated in the dialogue. This deepens the understanding of character motivations and relationships. The narrator helps in transitioning the story from one arc to another, maintaining narrative cohesion, especially when time jumps or significant events occur. At critical junctures, the narrator may provide reflective commentary, encouraging players to think about the implications of their choices or the events that have unfolded. CHAT HISTORY:{chat_history} MAIN CHARACTER: {user_input} NARRATOR RESPONSE:")

character_template = ChatPromptTemplate.from_template("Respond as {name}], who is {description}. They are {personality}. They have this aesthetic: {aesthetic}. In this scenario, we are in the act {act}. CHAT HISTORY:{chat_history} Our main character just said this Question/Interaction: {user_input} Character's Response:"
)
objective_evaluator = ObjectiveEvaluator(llm = ChatOpenAI(openai_api_key=openai_api_key, max_tokens=1000))
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit App
st.sidebar.title("Status:")
st.sidebar.markdown(f"Current Arc: **{current_arc['title']}**")
st.sidebar.markdown(f"Current Quest: **{current_quest['title']}**")
st.sidebar.markdown(f"Current Act: **{current_act['title']}**")
markdown_objective_list = "\n".join(f"- **{objective}**" for objective in current_objectives)
st.sidebar.markdown(f"Current Objectives\n{markdown_objective_list}")

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="narrator", content=f"Welcome to the world of: {title}")]
if "narrator_done" not in st.session_state:
    st.session_state["narrator_done"] = False
    
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    if not st.session_state["narrator_done"]:
        with st.chat_message("narrator"):
            
            stream_handler = StreamHandler(st.empty())
            llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler], max_tokens=100)
            narrator_chain = LLMChain(
                llm=llm, 
                prompt=narrator_template,
                verbose=True, 
                memory=chat_memory, 
                output_key='narrator'
            )
            response = narrator_chain({"title":title, "arc":current_arc, "quest":current_quest, "act":current_act, "objective":current_objectives[0], "user_input":prompt})
            print(response)
            content = response["narrator"]
            st.session_state.messages.append(ChatMessage(role="narrator", content=content))
            print('MEMORY',chat_memory)
            st.session_state["narrator_done"] = True
            
    with st.chat_message(cast[0]['name']):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler], max_tokens=1000)
        
        character_chain = LLMChain(
            llm=llm, 
            prompt=character_template,
            verbose=True, 
            memory=chat_memory,
            output_key="character")
        response = character_chain({"name":cast[0]['name'], "description":cast[0]['description'], "personality":cast[0]['personality'], "aesthetic":cast[0]['aesthetic'], "act":current_act, "user_input":prompt})
        content = response["character"]
        isObjectiveMet = objective_evaluator.chain({
            "last_messages":f"Human:{prompt} AI Character:{content}", 
            "detailed_objective":current_objectives[0]
            })
        print("isObjectiveMet",isObjectiveMet['completion_status'])
        if int(isObjectiveMet['completion_status']) > 50:
            print('Objective Met!')
            st.session_state['narrator_done'] = False
            st.toast(f"Objective{current_objectives[0]} Met!")
        else:
            # content = f"Objective Not Met! {content}"
            print("Objective Not Met!")
        st.session_state.messages.append(ChatMessage(role=f"{cast[0]['name']}", content=content))
        print('MEMORY',chat_memory)