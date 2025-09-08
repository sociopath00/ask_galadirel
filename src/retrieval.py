from typing import List

from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

import config


def retrieve_documents(client: QdrantClient,
                       query: str,
                       collection_name: str,
                       k: int) -> List:
    """Retrieve Top k documents from the Qdrant vector DB

    Args:
        client: Qdrant client object to setup a connection
        query: Search query from users
        collection_name: Name of the collection
        k: Int to return Top K results

    Returns:
        List of retrived documents. Size of the list is k
    """
    # Initialize embeddings (must match index.py)
    embeddings = OpenAIEmbeddings()
    sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

    # Connect to existing vector store
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        vector_name="dense",
        sparse_vector_name="sparse"
    )

    results = vectorstore.similarity_search(
        query=query,
        k=k,  
    )

    return results


if __name__ == "__main__":
    # Setup Qdrant client
    client = QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
        timeout=60.0,
    )

    query = "What was the age of Frodo in Long unexpected party?"

    results = retrieve_documents(client, query, collection_name=config.COLLECTION_NAME, k=5)

    for i, doc in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Content: {doc.page_content[:300]}...")