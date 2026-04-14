import os
from langchain_core.tools import tool
from ddgs import DDGS
import trafilatura
from langgraph.types import interrupt
from retriever import get_retriever

from config import MAX_TEXT_LENGTH, OUTPUT_DIR, REPORTS_DIR

@tool
def web_search(query: str) -> str:
    """Search for information on the internet. Returns a concise list of results."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    formatted = []
    for r in results:
        formatted.append(
            f"Title: {r.get('title')}\n"
            f"URL: {r.get('href')}\n"
            f"Snippet: {r.get('body')}\n"
        )

    return "\n---\n".join(formatted)

@tool
def read_url(url: str) -> str:
    """Fetches the full text content of a web page by URL."""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return "Error: could not download the page."

    text = trafilatura.extract(downloaded)
    if not text:
        return "Error: could not extract text from the page."

    text = text.strip()
    return text[:MAX_TEXT_LENGTH]

@tool
def write_report(filename: str, content: str) -> str:
    """Writes content to a Markdown file. filename must end with .md"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Report successfully saved to: {path}"


retriever = get_retriever()

@tool
def knowledge_search(query: str) -> str:
    """Search the local knowledge base. Use for questions about ingested documents."""
    docs = retriever(query)

    if not docs:
        return "Nothing found in the local knowledge base."

    results = []
    for i, doc in enumerate(docs):
        results.append(
            f"[Doc {i+1}]\n{doc.page_content[:500]}"
        )

    return "\n\n".join(results)


@tool
def save_report(filename: str, content: str) -> str:
    """Saves the final research report to a file. Requires human approval before writing."""
    decision = interrupt({"filename": filename, "content": content})

    if not isinstance(decision, dict):
        return "Unknown decision from user."

    action = decision.get("type")

    if action == "approve":
        os.makedirs(REPORTS_DIR, exist_ok=True)
        path = os.path.join(REPORTS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Report saved to: {path}"

    elif action == "reject":
        reason = decision.get("message", "no reason given")
        return f"Report saving rejected by user: {reason}"

    elif action == "edit":
        feedback = decision.get("feedback", "")
        return f"User requested changes to the report: {feedback}. Please revise the report based on this feedback and call save_report again."

    return "Unknown action."
