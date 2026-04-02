"""Chat-over-docs RAG agent — deployable via `langgraph dev`."""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# ---------------------------------------------------------------------------
# Document Loading & Indexing
# ---------------------------------------------------------------------------
URLS = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
]


def build_vectorstore() -> Chroma:
    """Load web documents, split them, and create a Chroma vector store."""
    loader = WebBaseLoader(URLS)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        collection_name="course_docs",
    )
    return vectorstore


vectorstore = build_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@tool
def search_documents(query: str) -> str:
    """Search the loaded documents for relevant information.

    Use this tool when the user asks questions about AI agents,
    prompt engineering, or related concepts from the articles.

    Args:
        query: The search query to find relevant document chunks.
    """
    docs = retriever.invoke(query)
    return "\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}"
        for d in docs
    )


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a knowledgeable AI assistant that helps users \
understand concepts from the loaded documents about AI agents and prompt \
engineering.

Rules:
- Always search the documents before answering questions about AI agents, \
prompt engineering, or related topics.
- Cite your sources when providing information from documents.
- If the documents don't contain relevant information, say so honestly.
- Be concise but thorough."""

agent = create_agent(
    model=init_chat_model("openai:gpt-4o-mini"),
    tools=[search_documents],
    prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)
