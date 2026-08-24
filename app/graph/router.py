from typing import Literal

from app.graph.state import GraphState
from app.llm.huggingface_client import HuggingFaceClient


Route = Literal["direct", "retrieve", "complex"]


class QueryRouter:
    """Adaptive RAG query router."""

    REPOSITORY_SIGNALS = (
        "repository", "repo", "source code", "codebase", "implementation",
        "implemented", "function", "class", "module", "file", "endpoint",
        "route", "configuration", "config", "error", "exception", "bug",
        "fastapi", "qdrant", "langgraph", "retriever", "reranker",
        "query router", "queryrouter", "rag pipeline", "workflow",
    )

    PROJECT_CONTEXT_SIGNALS = (
        "this project", "this repository", "this repo", "our project",
        "our code", "our codebase", "in the project", "in this codebase",
        "in this repository",
    )

    COMPLEX_SIGNALS = (
        "architecture", "workflow", "pipeline", "end-to-end", "trace",
        "how do these components", "how do the components", "compare",
    )

    def __init__(self, llm: HuggingFaceClient):
        self.llm = llm

    def route(self, state: GraphState) -> Route:
        question = state["question"].strip()
        question_lower = question.lower()

        has_project_context = any(signal in question_lower for signal in self.PROJECT_CONTEXT_SIGNALS)
        has_repository_signal = any(signal in question_lower for signal in self.REPOSITORY_SIGNALS)

        if has_project_context:
            if any(signal in question_lower for signal in self.COMPLEX_SIGNALS):
                return "complex"
            return "retrieve"

        if not has_repository_signal:
            return "direct"

        prompt = f"""
You are the routing controller for a software engineering RAG system.

Classify the user's question into exactly ONE category.

DIRECT: general knowledge; repository evidence is not required.
RETRIEVE: needs indexed repository documentation or source code.
COMPLEX: requires deeper repository investigation across multiple components.

Return ONLY one label:
DIRECT
RETRIEVE
COMPLEX

Question:
{question}

Label:
"""

        decision = self.llm.generate(prompt).strip().upper()

        if decision == "DIRECT":
            return "direct"
        if decision == "COMPLEX":
            return "complex"
        return "retrieve"
