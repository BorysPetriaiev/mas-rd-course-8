# 🤖 AI Research Agent

Персональний автономний агент.

Агент працює за циклом **ReAct** (Reasoning + Acting): він обмірковує запит, планує дії, використовує інструменти та формує фінальний аналітичний звіт.



## 🛠 Технологічний стек
- **Python 3.12**
- **uv** 
- **LangGraph** 
- **OpenAI**

## 📦 Встановлення та запуск

### 1. Підготовка середовища
Переконайтеся, що у вас встановлено інструмент [uv](https://docs.astral.sh/uv/).

```bash
# Клонуйте проєкт та перейдіть у папку
cd mas-rd-course-8

# Синхронізуйте залежності
uv sync
```


### 2. Налаштування конфіденційних даних
Створіть файл .env у кореневій директорії та додайте ваші ключі:

```
OPENAI_API_KEY=your_openai_key_here
```

### 3. Запуск агента

```bash
uv run ingest.py
uv run main.py
```

### Приклади запитів

- "Порівняй стратегії індексації: Flat, HNSW та IVF."
- "Досліди підхід Agentic RAG"

### Структура проєкту

```
mas-rd-course-5/
├── main.py              # REPL with HITL interrupt/resume loop
├── supervisor.py        # Supervisor agent + agent-as-tool wrappers
├── agents/
│   ├── __init__.py
│   ├── planner.py       # Planner Agent (uses ResearchPlan from schemas.py)
│   ├── research.py      # Research Agent (reuses hw5 tools)
│   └── critic.py        # Critic Agent (uses CritiqueResult from schemas.py)
├── schemas.py           # Pydantic models: ResearchPlan, CritiqueResult
├── tools.py             # Reused from hw5: web_search, read_url, knowledge_search + save_report
├── retriever.py         # Reused from hw5
├── ingest.py            # Reused from hw5
├── config.py            # Prompts + settings
├── requirements.txt     # Dependencies (add langgraph to hw5 deps)
├── data/                # Documents for RAG (from hw5)
└── .env                 # API keys (do not commit!)
└── output/              # Приклад звіту

```


### Приклад відпрацювання 
```
uv run main.py
warning: `VIRTUAL_ENV=/Users/boryspetriaiev/Desktop/mas-rd-course-5/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
🔄 Loading vector store...
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████| 201/201 [00:00<00:00, 6542.97it/s]
XLMRobertaForSequenceClassification LOAD REPORT from: BAAI/bge-reranker-base
Key                             | Status     |  | 
--------------------------------+------------+--+-
roberta.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED:   can be ignored when loading from different task/architecture; not ok if you expect identical arch.
🤖 Multi-agent research system ready! (type 'exit' to quit)
   Architecture: Supervisor → Planner → Researcher → Critic → save_report


You:  Compare RAG approaches: naive, sentence-window, and parent-child. Write a report.

🔧 [agent] plan(request='Compare RAG approaches: naive, sentence-window, and parent-child.')
   📎 [plan]: Research Plan:
Goal: To compare three approaches to Retrieval-Augmented Generation (RAG): Naive, Sentence-Window, and Parent-Child, highlighting their strengths, weaknesses, and performance metrics.
Search Queries:
  - Naive retrieval approach in RAG systems
  - Sentence-window retrieval in RAG syst

🔧 [agent] research(request="{'plan': {'goal': 'To compare three approaches to Retrieval-Augmented Generation (RAG): Naive, Sentence-Window, and Pare...")
   📎 [research]: Error invoking tool 'research' with kwargs {'request': {'plan': {'goal': 'To compare three approaches to Retrieval-Augmented Generation (RAG): Naive, Sentence-Window, and Parent-Child, highlighting their strengths, weaknesses, and performance metrics.', 'search_queries': ['Naive retrieval approach i

🔧 [agent] research(request='Compare three approaches to Retrieval-Augmented Generation (RAG): Naive, Sentence-Window, and Parent-Child, highlighting...')
   📎 [research]: ### Comparison of Retrieval-Augmented Generation (RAG) Approaches

Retrieval-Augmented Generation (RAG) is a framework that enhances the capabilities of large language models (LLMs) by integrating external information retrieval systems. This allows LLMs to generate responses based on both their pre-

🔧 [agent] critique(findings='### Comparison of Retrieval-Augmented Generation (RAG) Approaches\n\nRetrieval-Augmented Generation (RAG) is a framework t...')
   📎 [critique]: Critique Result:
Verdict: REVISE
Is Fresh: False
Is Complete: False
Is Well Structured: True
Strengths:
  + Comprehensive comparison of three RAG approaches
  + Clear strengths and weaknesses outlined for each approach
  + Well-organized structure with headings and a comparison table
Gaps:
  - Outda

🔧 [agent] research(request='Revise the report on RAG approaches by incorporating recent articles and findings from 2024-2026, adding information on ...')
   📎 [research]: ### Revised Report on Retrieval-Augmented Generation (RAG) Approaches

#### Introduction
Retrieval-Augmented Generation (RAG) has emerged as a pivotal methodology in enhancing the capabilities of large language models (LLMs) by integrating real-time data retrieval mechanisms. This report synthesizes

🔧 [agent] save_report(filename='RAG_Approaches_Comparison_Report.md', content='# Revised Report on Retrieval-Augmented Generation (RAG) Approaches\n\n## Introduction\nRetrieval-Augmented Generation (RAG...')

============================================================
⏸️  ACTION REQUIRES APPROVAL
============================================================
  Tool:  save_report
  File:  RAG_Approaches_Comparison_Report.md

  Content preview:

    # Revised Report on Retrieval-Augmented Generation (RAG) Approaches
    
    ## Introduction
    Retrieval-Augmented Generation (RAG) has emerged as a pivotal methodology in enhancing the capabilities of large language models (LLMs) by integrating real-time data retrieval mechanisms. This report synthesizes recent findings from 2024 to 2026, focusing on modular and agentic RAG systems, updated performance metrics, and case studies from recent implementations.
    
    ## 1. Overview of RAG Approaches
    RAG combines the strengths of information retrieval and generative models, allowing LLMs to access and utilize ext...
============================================================

👉 approve / edit / reject: approve
   📎 [save_report]: Report saved to: output/RAG_Approaches_Comparison_Report.md

🤖 [Agent]: The report comparing Retrieval-Augmented Generation (RAG) approaches has been successfully completed and saved. Here are the key details:

### Summary of the Report
- **Title**: Revised Report on Retrieval-Augmented Generation (RAG) Approaches
- **Content**: The report provides a comprehensive overview of three RAG approaches: Naive, Sentence-Window, and Parent-Child, along with recent developments in modular and agentic RAG systems. It includes updated performance metrics, case studies, and insights from the latest research (2024-2026).
- **Filename**: [RAG_Approaches_Comparison_Report.md](output/RAG_Approaches_Comparison_Report.md)

If you need any further assistance or additional information, feel free to ask!

You: exit
👋 Goodbye!
```