import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools import web_search, knowledge_search
from schemas import ResearchPlan
from config import PLANNER_PROMPT

load_dotenv()

_llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

planner_agent = create_react_agent(
    _llm,
    tools=[web_search, knowledge_search],
    prompt=PLANNER_PROMPT,
    response_format=ResearchPlan,
)
