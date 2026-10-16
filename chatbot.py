import os
import chainlit as cl

from dotenv import load_dotenv, find_dotenv
from agents import Agent, RunConfig,AsyncOpenAI, OpenAIChatCompletionsModel, Runner


load_dotenv(find_dotenv()) 

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider,
)


run_config = RunConfig(
    model=model,
    tracing_disabled=True,
)

agent1 = Agent(
    instructions="you are a helpful assistant that can answer question and help with tasks.",
    name="Hadi's Support Agent"
)


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello! I'm the Hadi's support Agent. How can I help you today?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history") or [] 

    history.append({"role": "user", "content": message.content}) 
    result =  await Runner.run(
        agent1,
        input=history,
        run_config=run_config
)
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()




