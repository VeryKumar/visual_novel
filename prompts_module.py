from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

# Prompt Templates for story generation
cast_template = PromptTemplate(
    input_variables=['title'],
    template="Write a list of characters with their persona for a story whose title is : {title}. Make each have a description, personality, and aesthetic. If its a story you know, make it novel but inspired by the source material. Output a JSON object"
)

arc_template = PromptTemplate(
    input_variables=['cast'],
    template="Write a list of arcs that our cast of characters will go on. Here are our characters: {cast}. An arc is a major plot device that all the cast is part of.Output a JSON object"
)
quest_template= PromptTemplate(
    input_variables=['arcs'],
    template="Write a list of quests that are important checkpoints for each arc of our story. Quests are a subset of arcs. Here are our generated arcs: {arcs}.Output a JSON object"
)

act_template =  PromptTemplate(
    input_variables=['quests'],
    template="Write a list of acts that make up the quests we have generated. Acts are a subset of quests. Here are our generated quests: {quests}. Output a JSON object"
)

objective_template = PromptTemplate(
    input_variables=['acts'],
    template="Given these story acts: {acts}, write a list of specific, actionable objectives for each arc. Each objective should be a concrete task or action that a character can perform, directly contributing to the progression of the story. Focus on clear and direct activities, avoiding abstract or broad goals. The objectives should involve interaction with the game environment, other characters, or personal development in a tangible way. They should be small-scale and precise, guiding the player through distinct, achievable steps crucial to the narrative of each arc. Output a JSON object"
)

story_template = PromptTemplate(
    input_variables=['cast', 'arcs', 'quests', 'acts'],
    template="Write a story according to the cast: {cast}. They will be going going on an adventure that is made up of these arcs: {arcs} and those arcs are made up of these quests: {quests}. Each of those quests are made of these acts: {acts}. Output a JSON object"
)
# Prompt templates for object generation

story_object_template = PromptTemplate(
    input_variables=['story_object_skeleton', 'story', 'objectives'],
    template="Generate a syntactically complete story_object with the information found in {story}. This is the skeleton you will build off of:{story_object_skeleton}. Make sure we have 2 arcs, 5 quests, 3 acts, and each act has 3-5 objectives. Here are our objectives: {objectives}. Output a JSON object"
)

# Prompt templates for character generation
#TODO: This could be part of the story engine. Decide where exposition should live

# narrator_template = PromptTemplate(
#     input_variables=["title","characters_in_the_scene", "arc", "quest", "act", "objective"],
#     template="DESCRIPTION: You are the narrator of a story called {title}. Right now the main character is trying to achieve the objective {objective}. The current world arc is: {arc}, which is made up of quests. The current quest is: {quest} which is made of acts. The current act is: {act}. The narrator is an omniscient and articulate entity, possessing a deep understanding of the story world and its characters. They are wise, often imparting subtle hints and insights about the plot and character motivations. The narrator is neutral in tone, maintaining a balance between detachment and empathy, allowing players to form their own emotional connections with the story. The narrator provides background information, setting the scene at the beginning of the story or a new chapter, Throughout the game, the narrator offers subtle guidance. This can include hints or suggestions, especially in moments of player indecision or confusion, but without giving away crucial plot points or making decisions for the player. The narrator occasionally offers insights into characters' thoughts or emotions that are not explicitly stated in the dialogue. This deepens the understanding of character motivations and relationships. The narrator helps in transitioning the story from one arc to another, maintaining narrative cohesion, especially when time jumps or significant events occur. At critical junctures, the narrator may provide reflective commentary, encouraging players to think about the implications of their choices or the events that have unfolded. NARRATOR RESPONSE:"
#     )

narrator_template = ChatPromptTemplate.from_template("DESCRIPTION: You are the narrator of a story called {title}. Right now the main character is trying to achieve the objective {objective}. The current world arc is: {arc}, which is made up of quests. The current quest is: {quest} which is made of acts. The current act is: {act}. The narrator is an omniscient and articulate entity, possessing a deep understanding of the story world and its characters. They are wise, often imparting subtle hints and insights about the plot and character motivations. The narrator is neutral in tone, maintaining a balance between detachment and empathy, allowing players to form their own emotional connections with the story. The narrator provides background information, setting the scene at the beginning of the story or a new chapter, Throughout the game, the narrator offers subtle guidance. This can include hints or suggestions, especially in moments of player indecision or confusion, but without giving away crucial plot points or making decisions for the player. The narrator occasionally offers insights into characters' thoughts or emotions that are not explicitly stated in the dialogue. This deepens the understanding of character motivations and relationships. The narrator helps in transitioning the story from one arc to another, maintaining narrative cohesion, especially when time jumps or significant events occur. At critical junctures, the narrator may provide reflective commentary, encouraging players to think about the implications of their choices or the events that have unfolded. NARRATOR RESPONSE:")


scene_template = PromptTemplate(
    input_variables=["title","characters_in_the_scene", "arc", "quest", "act", "objective"],
    template="Create a 1-2 sentence summary of the current scene given that we are in the story titled: {title}, The current world arc is {arc}, which is made up of quests. The current quest is: {quest} which is made of acts. The current act is: {act}. The current story objective is {objective}"
)

character_template = PromptTemplate(
    input_variables=["name", "description", "personality", "aesthetic", "act", "user_input"],
    template="Respond as {name}], who is {description}. They are {personality}. They have this aesthetic: {aesthetic}. In this scenario, we are in the act {act}. Our main character just said this Question/Interaction: {user_input} Character's Response:"
)
