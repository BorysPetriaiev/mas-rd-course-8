import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from agents.planner import planner_agent
from agents.research import researcher_agent
from agents.critic import critic_agent
from tools import save_report
from config import SUPERVISOR_PROMPT, MAX_FINDINGS_LEN

load_dotenv()


@tool
def plan(request: str) -> str:
    """Creates a structured research plan for the given request. Call this first."""
    result = planner_agent.invoke({"messages": [("user", request)]})
    plan_result = result.get("structured_response")
    if plan_result:
        queries = "\n".join(f"  - {q}" for q in plan_result.search_queries)
        sources = ", ".join(plan_result.sources_to_check)
        return (
            f"Research Plan:\n"
            f"Goal: {plan_result.goal}\n"
            f"Search Queries:\n{queries}\n"
            f"Sources to Check: {sources}\n"
            f"Output Format: {plan_result.output_format}"
        )
    return result["messages"][-1].content


@tool
def research(request: str) -> str:
    """Executes research based on the plan. Pass the plan and any critic feedback."""
    result = researcher_agent.invoke({"messages": [("user", request)]})
    return result["messages"][-1].content


@tool
def critique(findings: str) -> str:
    """Evaluates the quality of research findings. Returns structured verdict."""
    if len(findings) > MAX_FINDINGS_LEN:
        findings = findings[:MAX_FINDINGS_LEN] + "\n\n...[truncated for evaluation]"
    result = critic_agent.invoke({"messages": [("user", findings)]})
    critique_result = result.get("structured_response")
    if critique_result:
        strengths = "\n".join(f"  + {s}" for s in critique_result.strengths) or "  (none)"
        gaps = "\n".join(f"  - {g}" for g in critique_result.gaps) or "  (none)"
        revisions = "\n".join(f"  * {r}" for r in critique_result.revision_requests) or "  (none)"
        return (
            f"Critique Result:\n"
            f"Verdict: {critique_result.verdict}\n"
            f"Is Fresh: {critique_result.is_fresh}\n"
            f"Is Complete: {critique_result.is_complete}\n"
            f"Is Well Structured: {critique_result.is_well_structured}\n"
            f"Strengths:\n{strengths}\n"
            f"Gaps:\n{gaps}\n"
            f"Revision Requests:\n{revisions}"
        )
    return result["messages"][-1].content


_llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

supervisor = create_react_agent(
    _llm,
    tools=[plan, research, critique, save_report],
    prompt=SUPERVISOR_PROMPT,
    checkpointer=MemorySaver(),
)
