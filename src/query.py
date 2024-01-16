"""The query.py file defines the partition object, which is used for parsing
a partition name and returning the appropriate metadata filter.

This file implements a `query_documents` function that can be used to query
the knowledge base for documents under a given partition.
"""
import json
from typing import List

from canopy.context_engine import ContextEngine

from src.knowledge import ExpertKnowledgeBase
from src.partition import PartitionedQuery


def query_context(
    query: str, partition_name: str, max_context_tokens: int = 512
) -> List:
    """Query the knowledge base for documents under the given partition."""
    query = PartitionedQuery(query, partition_name)

    # Create a context engine
    kb = ExpertKnowledgeBase()
    context_engine = ContextEngine(kb)
    response = context_engine.query([query], max_context_tokens=max_context_tokens)
    result = json.loads(response.content.json())

    if not result:
        return ""

    context = result[0]
    snippets = [snippet["text"] for snippet in context["snippets"]]

    unique_snippets = []
    for snippet in snippets:
        if not any(snippet in s for s in snippets if s != snippet):
            unique_snippets.append(snippet)

    return "\n".join(unique_snippets)
