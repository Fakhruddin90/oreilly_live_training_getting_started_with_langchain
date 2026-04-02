# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

O'Reilly Live Training course teaching LangChain 1.0+ and LangGraph for building AI applications. The course covers agents, RAG systems, and complex AI workflows.

## LangChain 1.0+ Compliance (Important)

**All code in this repository must follow LangChain >= 1.0.0 documentation and patterns.** When writing or modifying code, always use the latest LangChain 1.0 APIs. Reference the official documentation at https://docs.langchain.com/ for current patterns.

### Deprecated → Current API Migration

| Deprecated (Pre-v1) | Current (v1.0+) |
|---------------------|-----------------|
| `create_react_agent()` | `create_agent()` |
| `create_tool_calling_agent()` | `create_agent()` |
| `AgentExecutor` | `create_agent()` returns a runnable graph directly |
| `langchain.chat_models.ChatOpenAI` | `langchain_openai.ChatOpenAI` |
| `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` |
| `langchain_community.tools.tavily_search.TavilySearchResults` | `langchain_tavily.TavilySearch` |
| `langchain.hub` | `langchain_classic.hub` (only for legacy prompts) |
| `ConversationBufferMemory` | Use LangGraph checkpointing or message history |
| `LLMChain` | Use LCEL (`prompt | model | parser`) |
| `SequentialChain` | Use LCEL with `RunnableSequence` |

### Key v1.0 Changes to Remember

1. **Agents return graphs**: `create_agent()` returns a LangGraph `CompiledGraph`, not an executor
2. **Messages-based I/O**: Agents use `{"messages": [...]}` format, not `{"input": "..."}`
3. **Python 3.10+ required**: Python 3.9 is no longer supported
4. **Separate packages**: Use provider-specific packages (`langchain-openai`, `langchain-anthropic`, etc.)

## Development Commands

```bash
# Setup (uv-based)
uv sync                     # Install all dependencies
uv run jupyter lab           # Launch Jupyter

# Or use the Makefile
make setup                   # uv sync
make run                     # uv run jupyter lab
make demo                    # Run the demo agent with langgraph dev
```

## Required Environment Variables

```bash
# Copy .env.example and fill in your keys
cp .env.example .env

OPENAI_API_KEY="..."
TAVILY_API_KEY="..."                  # For search tools
LANGSMITH_API_KEY="..."               # Optional: LangSmith tracing
LANGSMITH_TRACING=true                # Enable tracing
LANGSMITH_PROJECT=oreilly-langchain   # Project name in LangSmith
```

## LangChain 1.0 Patterns (Critical)

This codebase uses LangChain 1.0+ patterns. Key differences from pre-v1:

### Agent Creation
```python
# LangChain 1.0 pattern (use this)
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",  # String format
    tools=tools,
    system_prompt="...",
)
result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})

# NOT the old AgentExecutor pattern
```

### Tool Definition
```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool docstring becomes the tool description."""
    return result
```

### Streaming
```python
# Token-by-token streaming
for token, metadata in agent.stream({"messages": "..."}, stream_mode="messages"):
    print(token.content, end="")

# State streaming
for step in agent.stream({"messages": "..."}, stream_mode="values"):
    step["messages"][-1].pretty_print()
```

### Runtime Context (Dependency Injection)
```python
from dataclasses import dataclass
from langgraph.runtime import get_runtime

@dataclass
class RuntimeContext:
    db: SQLDatabase

@tool
def execute_sql(query: str) -> str:
    runtime = get_runtime(RuntimeContext)
    return runtime.context.db.run(query)

agent = create_agent(..., context_schema=RuntimeContext)
agent.invoke({...}, context=RuntimeContext(db=db))
```

## Repository Structure

- `notebooks/` - Course Jupyter notebooks (1.0 Fundamentals, 2.0 Structured Outputs)
- `demo/` - Deployable Chat-Over-Docs RAG agent (langgraph.json + agent.py)
- `scripts/` - Standalone Python examples (supplementary reference)
- `deprecated/` - Pre-April 2026 course notebooks
- `archive/pre-v1/` - Legacy pre-LangChain-1.0 notebooks (reference only)
- `pyproject.toml` - Dependencies managed via uv

## Import Conventions

```python
# Models
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

# Core
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool

# Agents
from langchain.agents import create_agent

# Structured Output
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy

# Search (LangChain 1.0)
from langchain_tavily import TavilySearch  # NOT langchain_community.tools.tavily_search

# Memory
from langgraph.checkpoint.memory import InMemorySaver
```
