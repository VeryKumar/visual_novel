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

# Story Progression Variables
isObjectiveMet = {'completion_status': 0}

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
            
def isObjectiveMetChain(human_message, ai_message, current_objective):
            objective_evaluator = ObjectiveEvaluator(llm = ChatOpenAI(openai_api_key=openai_api_key, max_tokens=1000))
            response = objective_evaluator.chain({
            "last_messages":f"Human:{human_message} AI Character:{ai_message}", 
            "detailed_objective":current_objective
            })
            isObjectiveMet['completion_status'] = response['completion_status']

# LANGCHAIN LOGIC 

#
chat_memory = ConversationBufferMemory(memory_key='chat_history', input_key='user_input')   

narrator_template = ChatPromptTemplate.from_template("DESCRIPTION: You are the narrator of a story called {title}. Right now the main character is trying to achieve the objective {objective}. The current world arc is: {arc}, which is made up of quests. The current quest is: {quest} which is made of acts. The current act is: {act}. The narrator is an omniscient and articulate entity, possessing a deep understanding of the story world and its characters. They are wise, often imparting subtle hints and insights about the plot and character motivations. The narrator is neutral in tone, maintaining a balance between detachment and empathy, allowing players to form their own emotional connections with the story. The narrator provides background information, setting the scene at the beginning of the story or a new chapter, Throughout the game, the narrator offers subtle guidance. This can include hints or suggestions, especially in moments of player indecision or confusion, but without giving away crucial plot points or making decisions for the player. The narrator occasionally offers insights into characters' thoughts or emotions that are not explicitly stated in the dialogue. This deepens the understanding of character motivations and relationships. The narrator helps in transitioning the story from one arc to another, maintaining narrative cohesion, especially when time jumps or significant events occur. At critical junctures, the narrator may provide reflective commentary, encouraging players to think about the implications of their choices or the events that have unfolded. CHAT HISTORY:{chat_history} MAIN CHARACTER: {user_input} NARRATOR RESPONSE:")

# bridging_narrator_template = ChatPromptTemplate.from_template("""DESCRIPTION: You are the 'Bridging Narrator' of a story called {title}. Your role is pivotal in transitioning the main character from the recently completed objective {last_objective} to the next objective {next_objective}. The current world arc is: {arc}, which unfolds through a series of quests. The character has just completed the quest: {last_quest}, and is about to embark on: {next_quest}. The current act within this quest is: {act}. The 'Bridging Narrator' is an omniscient and articulate entity, with an insightful understanding of the story world, its history, and its future directions. You have a keen perception of character growth and plot development. You are highly skilled at your job. Your tone is informative yet engaging, connecting past achievements with future challenges. You set the stage for transitions by summarizing key accomplishments, highlighting the significance of the completed objective, and creating anticipation for the upcoming challenge. In this role, you provide a reflective analysis of the character’s journey, offering insights into how past decisions and actions have shaped the current state of affairs and will influence future events. You also hint at potential consequences and opportunities that lie ahead, without revealing crucial plot points. Your narration is a blend of retrospective and prospective storytelling, weaving the old and new objectives into a coherent, compelling narrative thread. You help players appreciate the continuity and evolution of the story, ensuring they remain immersed and motivated as they progress from one objective to the next. You introduce the next high tension event that will continue the story. Instead of simply summarizing, introduce events that push the forwards.NARRATOR RESPONSE:""")

# V2
# bridging_narrator_template = ChatPromptTemplate.from_template("""
# "DESCRIPTION: As the 'Bridging Narrator' in the story titled {title}, your primary role is to dynamically transition the main character from their completed objective, {last_objective}, to their next challenge, {next_objective}. You're navigating the narrative through the current world arc: {arc}, marked by a sequence of action-packed quests. The character has just conquered the quest: {last_quest}, and is poised to embark on an adventurous journey in: {next_quest}, currently at the act: {act}.

# Your narration is unique, characterized by an omniscient, articulate perspective that not only recounts events but actively shapes them. You're adept at injecting excitement and momentum into the story, setting up thrilling scenarios and unexpected encounters.

# Your narration style is less about exposition and more about action and reaction. You create vivid, dynamic scenes where the character's decisions instantly lead to new developments. For instance, as soon as the character achieves a goal, they might be ambushed by a rival, discover a mysterious artifact, or receive an urgent message that propels them into the next phase of their journey.

# In this role, you balance the story's past and future by emphasizing immediate action and direct consequences. You craft scenes that are rich with potential conflicts and plot twists, keeping players on the edge of their seats. Your skill lies in your ability to weave these events seamlessly into the ongoing narrative, maintaining a continuous flow while escalating the stakes.

# You will introduce the next high-tension event, like a sudden attack, a betrayal, or an unexpected alliance, to propel the story forward. Your goal is to keep the narrative engaging and fast-paced, focusing on actions and events that drive the plot rather than introspective analysis.

# NARRATOR RESPONSE:""")

# V3
bridging_narrator_template = ChatPromptTemplate.from_template("""DESCRIPTION: In your role as the 'Bridging Narrator' for a gripping story, you have the unique task of guiding the main character from one pivotal moment to the next without directly mentioning the titles of objectives, quests, or the story arc. You're the unseen hand that subtly steers the narrative, connecting the just-concluded triumph to an imminent challenge.

Your narrative style is nuanced and layered, rich with implicit references to the character's past achievements and future endeavors. Instead of explicitly stating the last or next objectives, you create scenarios that naturally lead the protagonist from one point to another. You craft your narration through actions and events that hint at what has just been accomplished and what lies ahead.

For instance, after a significant victory, the character might find a clue that hints at their next destination or challenge. You could describe the character's reaction to this discovery, setting the stage for what's to come. Your expertise lies in maintaining the suspense and excitement of the journey without explicitly revealing the names of quests or objectives.

Your role is to weave a narrative that feels organic and fluid, where the story's progression feels like a natural consequence of the character's actions and decisions. You focus on creating moments of tension and surprise, introducing elements like unexpected encounters, mysterious messages, or sudden changes in the character's environment that signal the beginning of a new chapter in their journey.

As the narrator, you provide a descriptive yet enigmatic overview of the character's journey, using imagery and metaphor to allude to the bigger picture. You ensure that the players remain deeply engaged, curious about the character's next move, and eager to uncover the story's unfolding mysteries.

NARRATOR RESPONSE:""")


character_template = ChatPromptTemplate.from_template("Respond as {name}], who is {description}. They are {personality}. They have this aesthetic: {aesthetic}. In this scenario, we are in the act {act}. CHAT HISTORY:{chat_history} Our main character just said this Question/Interaction: {user_input} Character's Response:"
)

# objective_evaluator = ObjectiveEvaluator(llm = ChatOpenAI(openai_api_key=openai_api_key, max_tokens=1000))
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

if 'narrator_intro_done' not in st.session_state:
    st.session_state['narrator_intro_done'] = False

if 'objective_completed' not in st.session_state:
    st.session_state['objective_completed'] = False
    
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    if not st.session_state['narrator_intro_done']:
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
            st.session_state["narrator_intro_done"] = True
            
    with st.chat_message(cast[0]['name']):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler], max_tokens=1000)
        
        character_chain = LLMChain(
            llm=llm, 
            prompt=character_template,
            verbose=True, 
            memory=chat_memory,
            output_key="character"
        )
        response = character_chain({"name":cast[0]['name'], "description":cast[0]['description'], "personality":cast[0]['personality'], "aesthetic":cast[0]['aesthetic'], "act":current_act, "user_input":prompt})
        content = response["character"]
        
        isObjectiveMetChain(human_message=prompt, ai_message=content, current_objective=current_objectives[0])
        
        print("isObjectiveMet",isObjectiveMet['completion_status'])
        
        if int(isObjectiveMet['completion_status']) > 50:
            print('Objective Met!')
            st.session_state['narrator_done'] = False
        else:
            # content = f"Objective Not Met! {content}"
            print("Objective Not Met!")
        st.session_state.messages.append(ChatMessage(role=f"{cast[0]['name']}", content=content))
        print('MEMORY',chat_memory)
        
    
    if int(isObjectiveMet['completion_status']) > 50 and not st.session_state['objective_completed']:
        print('Objective Met!')
        st.toast(f"Objective {current_objectives[0]} Met!")
        # Narrator speaks when an objective is met
        with st.chat_message("narrator"):
            stream_handler = StreamHandler(st.empty())
            llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler], max_tokens=1000)
            bridging_narrator_chain = LLMChain(
            llm=llm, 
            prompt=bridging_narrator_template, 
            verbose=True, 
            memory=chat_memory, 
            output_key='bridging_narrator'
            )
            response = bridging_narrator_chain({
            "title": title, 
            "last_objective": current_objectives[0],  # Define this variable based on your game logic
            "next_objective": current_objectives[1],  # Define this variable based on your game logic
            "arc": current_arc, 
            "last_quest": current_quest,  # Define this variable based on your game logic
            "next_quest": current_quest,  # Define this variable based on your game logic
            "act": current_act,
            "user_input": prompt
        })
            # completion_message = f"Objective '{current_objectives[0]}' completed successfully. Well done!"
            content = response["bridging_narrator"]
            st.session_state.messages.append(ChatMessage(role="narrator", content=content))
            st.session_state.objective_completed = True
    else:
        print("Objective Not Met!")