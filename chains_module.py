from langchain.chains import LLMChain, SequentialChain
from llms_module import llm
from prompts_module import cast_template, story_template, arc_template, quest_template, act_template
from memory_module import story_memory, cast_memory

# Chains
cast_chain = LLMChain(llm=llm, prompt=cast_template,
                      verbose=True, output_key='cast', memory=cast_memory)

arc_chain = LLMChain(llm=llm, prompt=arc_template,
                     verbose=True, output_key='arcs')

quest_chain = LLMChain(llm=llm, prompt=quest_template,
                       verbose=True, output_key='quests')

act_chain = LLMChain(llm=llm, prompt=act_template,
                       verbose=True, output_key='acts')

story_chain = LLMChain(llm=llm, prompt=story_template,
                       verbose=True, output_key='story', memory=story_memory)
# sequential_chain = SequentialChain(
#     chains=[cast_chain, story_chain], input_variables=['title'], output_variables=['cast', 'story'], verbose=True)