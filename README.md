# AIA Knowledge Base Management

This repository creates an evironment for managing the knowledge bases of the
AIA. The only feature of this knowledge base for know is a webhook sever which
integrates Canopy. For more information on canopy, please read this
[atricle](https://www.pinecone.io/blog/canopy-rag-framework/).

## Canopy Webhook Server

We want to build a webhook server that has two main endpoints:

- `/store`: An endpoint that allows us to store data in a patricular experts
  knowledge base. We will tag each vector that we create for the post with the
  name of the post.
- `/query`: An endpoint that takes a natural language query, an expert name, and
  a max token limit. The server will query the supplied partiton and return the
  most relevant context up to the max token limit.
