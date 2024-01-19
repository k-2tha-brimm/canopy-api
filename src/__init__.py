"""Setup the src module for use in the Canopy project."""
import os

from dotenv import load_dotenv
from canopy.tokenizer import Tokenizer

# Load the .env file
load_dotenv()

# Ensure that all the necessary .env variables are loaded
INDEX_NAME = os.getenv("INDEX_NAME")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
POSTGRESQL_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")

print(f"INDEX_NAME: {INDEX_NAME}")
print(f"PINECONE_API_KEY: {PINECONE_API_KEY}")
print(f"PINECONE_ENVIRONMENT: {PINECONE_ENVIRONMENT}")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")
print(f"POSTGRESQL_DATABASE_URL: {POSTGRESQL_DATABASE_URL}")

assert INDEX_NAME, "INDEX_NAME not found in .env"
assert PINECONE_API_KEY, "PINECONE_API_KEY not found in .env"
assert PINECONE_ENVIRONMENT, "PINECONE_ENVIRONMENT not found in .env"
assert OPENAI_API_KEY, "OPENAI_API_KEY not found in .env"
assert POSTGRESQL_DATABASE_URL, "OPENAI_API_KEY not found in .env"

# Intialize the tokenizer for use throughout the src module
Tokenizer.initialize()
