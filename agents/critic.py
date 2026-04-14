import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools import web_search, read_url, knowledge_search
from schemas import CritiqueResult
from config import CRITIC_PROMPT

load_dotenv()

_llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

critic_agent = create_react_agent(
    _llm,
    tools=[web_search, read_url, knowledge_search],
    prompt=CRITIC_PROMPT,
    response_format=CritiqueResult,
)
