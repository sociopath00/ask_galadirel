import glob

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, SparseVectorParams, VectorParams

import config
from src.loggers import logger


def check_and_delete(client: QdrantClient,
                     collection_name: str):
    """Check if collection exists or not and Delete if it already exists

    Args:
        client: Qdrant client object to setup a connection
        collection_name: Name of the collection 

    Return:
        Boolean value. True if collections exists(and deleted) else False
    """
    collections = [i.name for i in client.get_collections().collections]

    if collection_name in collections:
        client.delete_collection(collection_name=collection_name)
        return True
    else:
        return False


def embedding_and_indexing(client: QdrantClient,
                           data_dir: str,
                           collection_name: str,
                           chunk_size: int,
                           chunk_overlap: int,
                           vector_embedding_model: str="text-embedding-3-small",
                           vector_size: int=1536,
                           sparse_embedding_model: str="Qdrant/bm25"):
    """Create a new collection. Read the PDF documents and create embeddings
    and store it in Qdrant vectorDB

    Args:
        client: Qdrant client object to setup a connection
        data_dir: Data directory where PDF documents are stored
        collection_name: Name of the collection to be created
        chunk_size: Chunk size for splitting the documents
        chunk_overlap: Overlapping while splitting the documents
        vector_embedding_model: Model to be used for dense vector creation (default: text-embedding-3-small)
        vector_size: Length of the vector_embedding_model (default: 1536)
        sparse_embedding_model: Model to be used for sparse embedding creation (default: Qdrant/bm25)
    """
    # Check if collection exists, delete if it exists
    status = check_and_delete(client=client, collection_name=collection_name)
    if status:
        logger.debug(f"Deleted the old collection: {collection_name}")

    # Loop over all the PDFs inside data_dir and create a list of documents
    all_docs = []
    for filepath in glob.glob(data_dir):
        logger.debug(f"Reading the PDF file {filepath}")
        loader = PyPDFLoader(filepath)
        docs = loader.lazy_load()
        all_docs.extend(docs)

    logger.info("Chunking process has started")
    # Chunking and splittig the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap)
    documents = text_splitter.split_documents(all_docs)

    # Initialize embedding
    embeddings = OpenAIEmbeddings(model=vector_embedding_model)     # default embedding model: text-embedding-3-small
    sparse_embeddings = FastEmbedSparse(model_name=sparse_embedding_model)
    
    # Create a new collection with both Dense and Sparse vectors
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"dense": VectorParams(size=vector_size, distance=Distance.COSINE)}, # vector size for text-embedding-3-small is 1536
        sparse_vectors_config={
            "sparse": SparseVectorParams(index=models.SparseIndexParams(on_disk=False))
        },
    )
    logger.info(f"New collection is created: {collection_name}")

    # Store the document in Vector Store
    # Default indexing is HNSW 
    doc_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        vector_name="dense",
        sparse_vector_name="sparse"
    )

    doc_store.add_documents(documents)
    logger.info("All the documents are stored in Qdrant vector db")
    return None


if __name__ == "__main__":
    # Setup Qdrant client
    client = QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
        timeout=120.0  # increase timeout for large inserts
    )

    embedding_and_indexing(client, config.DATA_DIR, config.COLLECTION_NAME, config.CHUNK_SIZE, config.CHUNK_OVERLAP)