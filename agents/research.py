import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools import web_search, read_url, knowledge_search
from config import RESEARCHER_PROMPT

load_dotenv()

_llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

researcher_agent = create_react_agent(
    _llm,
    tools=[web_search, read_url, knowledge_search],
    prompt=RESEARCHER_PROMPT,
)
