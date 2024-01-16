# Canopy Webhook Server Documentation

The Canopy webhook server has 2 basic endpoints:

- PUT `/document`: For the contents of a document in a partition of the
  knowledge base
- GET `/context`: For retrieving context from a knowledge base partition with a
  query

It is hosted on a simple AWS EC2 instance, and is implemented as an HTTP server
using a Dockerized FastAPI application.

## Connexting to the Server

The server can be accessed via HTTP, at its two endpoints. The base url of the
API is: `http://18.119.84.34/`.

In order to receive a successful response, you must send your request to adhere
strictly to the schema defined by one of the two endpoints.

## PUT `/document`

This endpoint is used for storing the contents of a document. It's request
payload has a simple structure:

```json
{
  "content": "<document_content: str>",
  "partition_name": "<partion_arn:str>"
}
```

The parition should be formatted in the following format:
`expert_name:document_name`. Please note, that paritions are only setup to
support two layers. Attempt to use more than 2 layers in a partition will result
in an error.

The response payload of the endpoint simply reutrns the ID of the newly stored
document:

```json
{
  "document_id": "<document_id: str>"
}
```

## GET `/context`

This endpoint is used for storing the querying the context stored in a certain
partition. The GET method required two query parameters and one optional query
arameter:

- `query` (`str`): The query to search for relevant context
- `partition_name` (`str`): The name of the partition you want to query.
- `max_context_tokens` (`Optional[str]`): The max number of context tokens to
  return (Default 512)

The response payload of the endpoint simply returns the relevant context from
the partition, up to the specified `max_context_tokens`

```json
{
  "context": "<relevant_context: str>"
}
```
