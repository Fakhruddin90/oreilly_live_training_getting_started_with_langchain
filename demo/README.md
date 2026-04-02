# Chat Over Docs — Demo Application

A deployable RAG agent that answers questions about AI agent research papers.

## Quick Start

1. From the **repo root**, ensure dependencies are installed:

   ```bash
   uv sync
   ```

2. Copy your `.env` file into the demo folder (or run `make demo` which does this automatically):

   ```bash
   cp ../.env .env
   ```

3. Start the local development server:

   ```bash
   uv run langgraph dev
   ```

   The server starts at `http://127.0.0.1:2024` with hot-reloading.

4. Connect the Agent Chat UI:

   ```bash
   npx @langchain/agent-chat-ui
   ```

   Open `http://localhost:3000`, then enter:
   - **Deployment URL**: `http://localhost:2024`
   - **Graph ID**: `chat_over_docs`

   Or visit [agentchat.vercel.app](https://agentchat.vercel.app) and connect there.

## Architecture

- `agent.py` — RAG agent: loads web docs, creates vector store, exposes retrieval tool
- `langgraph.json` — LangGraph deployment configuration

## Observability

With `LANGSMITH_TRACING=true` in your `.env`, all agent runs are automatically traced to [LangSmith](https://smith.langchain.com/). You can see:
- Tool calls and retriever results
- Token usage per step
- Full conversation history
