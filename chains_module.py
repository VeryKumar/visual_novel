from langchain.chains import LLMChain, SequentialChain
from llms_module import  jsonModeModel, llm
from prompts_module import cast_template, arc_template, quest_template, act_template, objective_template, story_template, story_object_template, narrator_template, scene_template, character_template
from memory_module import story_memory, cast_memory, story_object_memory
from langchain_core.output_parsers import StrOutputParser


#EXPERIMENT: MOVE LLM HERE


# Story Chains
cast_chain = LLMChain(llm=jsonModeModel, prompt=cast_template,
                      verbose=True, output_key='cast', memory=cast_memory)

arc_chain = LLMChain(llm=jsonModeModel, prompt=arc_template,
                     verbose=True, output_key='arcs')

quest_chain = LLMChain(llm=jsonModeModel, prompt=quest_template,
                       verbose=True, output_key='quests')

act_chain = LLMChain(llm=jsonModeModel, prompt=act_template,
                       verbose=True, output_key='acts')

objective_chain = LLMChain(llm=jsonModeModel, prompt=objective_template,
                           verbose=True, output_key='objectives')

story_chain = LLMChain(llm=jsonModeModel, prompt=story_template,
                       verbose=True, output_key='story', memory=story_memory)

# Character chains

narrator_chain = LLMChain(llm=llm, prompt=narrator_template,
                          verbose=True, output_key='narrator')

# narrator_chain = narrator_template | llm | StrOutputParser()

scene_chain = LLMChain(llm=llm, prompt=scene_template,
                          verbose=True, output_key="scene")

character_chain = LLMChain(llm=llm, prompt=character_template,
                           verbose=True, output_key="character")

# Structured Chains

story_object_chain = LLMChain(llm=jsonModeModel, prompt=story_object_template,
                       verbose=True, output_key='story_object', memory=story_object_memory)

