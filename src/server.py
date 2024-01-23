"""The FastAPI server implementation."""
import requests
from typing import Optional, List
from lxml import html

from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from src.knowledge import store_document
from src.query import query_context
from src import models, schemas
from src.database import get_db

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

    response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={
        'action': 'parse',
        'format': 'json',
        'page': partition_name,
        'prop': 'text',
        'redirects':''
    }).json()
    raw_html = response['parse']['text']['*']
    document = html.document_fromstring(raw_html)

    text = ''
    for p in document.xpath('//p'):
        text += p.text_content() + '\n'

    return {"context": context, "text": text}


@app.get('/files', response_model=List[schemas.CreateFile])
def test_files(db: Session = Depends(get_db)):

    files = db.query(models.File).all()

    return files


@app.get('/files/{filename}', response_model=schemas.CreateFile, status_code=status.HTTP_200_OK)
def get_test_one_file(filename:str, db:Session = Depends(get_db)):

    file = db.query(models.File).filter(models.File.filename == filename).first()

    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The filename: {filename} you requested for does not exist")
    return file


@app.post('/files', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreateFile])
def test_file_sent(post_file:schemas.CreateFile, db:Session = Depends(get_db)):

    new_file = models.File(**post_file.dict())
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return [new_file]
