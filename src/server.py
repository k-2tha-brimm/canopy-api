"""The FastAPI server implementation."""
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from src.knowledge import store_document
from src.query import query_context

app = FastAPI()

origins = [
    "https://file-upload-ui.netlify.app",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DocumentPayload(BaseModel):
    """The payload for the document."""

    content: str
    partition_name: str


@app.put("/document")
def put_document(document: DocumentPayload):
    # Using partition_name as the key to store the content
    try:
        # Store the document in the knowledge base
        doc = store_document(document.content, document.partition_name)

        # Return the document ID to the caller
        return {"document_id": doc.id}
    except Exception as exp:  # pylint: disable=broad-except
        print(exp)
        raise HTTPException(
            status_code=500, detail="Error while saving the document"
        ) from exp


@app.get("/context")
def get_context(
    query: Optional[str] = Query(None),
    partition_name: Optional[str] = Query(None),
    max_context_tokens: Optional[int] = 512,
):
    """Get the document context for the given query."""
    # Check if partition_name is provided and exists
    if partition_name is None:
        raise HTTPException(
            status_code=400, detail="Query parameter `partition_name` not provided"
        )
    if query is None:
        raise HTTPException(
            status_code=400, detail="Query parameter `query` not provided"
        )

    if not isinstance(max_context_tokens, int):
        raise HTTPException(
            status_code=400,
            detail="Query parameter `max_context_tokens` must be an integer",
        )

    context = query_context(
        query, partition_name, max_context_tokens=max_context_tokens
    )
    return {"context": context}
