"""The knowledge.py file defines all the objects that are used for storing data.

To make things simple, the file only has one exported member, which is the 
`store_data` function. This function is called by the `/store` endpoint.
"""
import os
from typing import List

from canopy.knowledge_base import KnowledgeBase
from canopy.knowledge_base.chunker.base import Chunker
from canopy.knowledge_base.models import KBDocChunk
from canopy.models.data_models import Document
from canopy.tokenizer import Tokenizer

from src.partition import PartitionedDocument

# The name of the Pinecone index to use for the knowledge base
INDEX_NAME = os.getenv("INDEX_NAME")


class TokenLengthChunker(Chunker):
    """A document chunker that chunks documents based on the number of tokens.

    We want to create varied sized chunks of documents. This chunker will recursively
    chunk the document following this pattern:
        - N chunks of 64 tokens
        - N / 2 chunks of 128 tokens
        - N / 4 chunks of 256 tokens
        - N / 8 chunks of 512 tokens

    This process will be terminated early if the document is less than 512 tokens (or
    256 tokens, 128 tokens, etc.)
    """

    def __init__(self):
        self.tokenizer = Tokenizer()

        # The chunk sizes that we make chunks for
        self.sizes = [64, 128, 256, 512]

    def _make_chunks(
        self, document: Document, tokens: List[str], chunk_size: int
    ) -> List[KBDocChunk]:
        """Make chunks of the given size from the given tokens.

        Args:
            tokens (List[str]): The tokens to chunk
            chunk_size (int): The size of the chunks

        Returns:
            List[KBDocChunk]: The list of chunks
        """
        chunks = []

        print(f"Making chunks of size {chunk_size} for document {document.id}")

        # Iterate over the document tokens in chunks of the given size
        for i in range(0, len(tokens), chunk_size):
            # Create the chunk text by detokenizing the tokens and compute the index of the chunk
            chunk_text = self.tokenizer.detokenize(tokens[i : i + chunk_size])
            chunk_index = i // chunk_size

            chunk = KBDocChunk(
                # Id the chunk by the document id, the chunk size, and the chunk index
                id=f"{document.id}-{chunk_size}-{chunk_index}",
                document_id=document.id,
                text=chunk_text,
                source=document.source,
                metadata=document.metadata,
            )
            chunks.append(chunk)

        return chunks

    def chunk_single_document(self, document: Document) -> List[KBDocChunk]:
        """Chunk a single document into multiple chunks.

        Args:
            document (KBDocChunk): The document to chunk

        Returns:
            List[KBDocChunk]: The list of chunks
        """
        # Tokenize the document text
        tokens = self.tokenizer.tokenize(document.text)
        chunk_sizes = [size for size in self.sizes if size <= len(tokens)]

        # If the doucment is less than 64 tokens, we will simply chunk the entire document
        # as one chunk
        if not chunk_sizes:
            chunks = self._make_chunks(document, tokens, len(tokens))
            return chunks

        print(
            f"Chunking document {document.id} into {len(chunk_sizes)} different chunk sizes"
        )
        # Otherwise, if the document is at least 64 tokens, we will chunk it into multiple
        # chunks of varying sizes
        chunks = []
        for size in chunk_sizes:
            new_chunks = self._make_chunks(document, tokens, size)
            chunks.extend(new_chunks)

        print(f"Chunked document {document.id} into {len(chunks)} chunks")
        return chunks

    async def achunk_single_document(self, document: Document) -> List[KBDocChunk]:
        """Async implementation of document chunking."""
        raise NotImplementedError()


class ExpertKnowledgeBase(KnowledgeBase):
    """The Knowledge Base for the AIA Experts. Managed through Canopy."""

    def __init__(self, index_name: str = INDEX_NAME, chunker: Chunker = None):
        # Set the default Chunker if none is provided
        if not chunker:
            chunker = TokenLengthChunker()

        # Instantiate the KnowledgeBase class
        super().__init__(index_name=index_name, chunker=chunker)

        # Connect to the index
        self.connect()

    def upsert(
        self,
        documents: List[Document],
        namespace: str = "",
        batch_size: int = 200,
        show_progress_bar: bool = False,
    ):
        """Upsert the given documents into the knowledge base.

        Args:
            documents (List[Document]): The documents to upsert
        """

        super().upsert(
            documents,
            namespace=namespace,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
        )


def store_document(content: str, partition_name: str) -> Document:
    """Create a chunked document and store the chunks under the
    given partition name.

    Args:
        content (str): The content of the document
        partition_name (str): The name of the partition to store the document under
    """

    # Create a document object
    doc = PartitionedDocument(partition_name, content)

    # Create a knowledge base object
    kb = ExpertKnowledgeBase()

    # Upsert the document into the knowledge base
    kb.upsert([doc])

    return doc
