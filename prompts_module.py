from langchain.prompts import PromptTemplate

# Prompt Template
cast_template = PromptTemplate(
    input_variables=['title'],
    template="Write a list of characters with their persona for a story whose title is : {title}"
)

arc_template = PromptTemplate(
    input_variables=['cast'],
    template="Write a list of arcs that our cast of characters will go on. Here are our characters: {cast}. An arc is a major plot device "
)
quest_template= PromptTemplate(
    input_variables=['arcs'],
    template="Write a list of quests that are important checkpoints for each arc of our story. Quests are a subset of arcs. Here are our generated arcs: {arcs}."
)

act_template =  PromptTemplate(
    input_variables=['quests'],
    template="Write a list of acts that make up the quests we have generated. Acts are a subset of quests. Here are our generated quests: {quests}."
)
 
story_template = PromptTemplate(
    input_variables=['cast', 'arcs', 'quests', 'acts'],
    template="Write a story according to the cast which are {cast}. They will be going going on an adventure that is made up of these arcs: {arcs} and those arcs are made up of these quests: {quests}. Each of those quests are made of these acts: {acts}."
)


