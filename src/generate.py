from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.loggers import logger
from src.retrieval import retrieve_documents
from qdrant_client import QdrantClient
import config


def generate_answer(query: str,
                    results: list,
                    model_name: str="gpt-4o-mini") -> str:
    """Generate the answers based on provided context for the given query

    Args:
        query: User's query
        results: Context retrived from the vector db
        model_name: Name of the model used for answer generation (Default: gpt-4o-mini)

    Returns:
        String of generated answer
    """
    logger.info("Stating the generation")

    # Concatenate context
    context = "\n\n".join([result.page_content for result in results])

    # Prepare the prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"{config.SYS_PROMPT}"),
        ("user", "Context:\n{context}\n\nQuestion: {question}")
    ])

    # Initialize the model
    llm = ChatOpenAI(model=model_name, temperature=0)

    # Create the chain
    chain = prompt | llm

    # Generate the response
    response = chain.invoke({
        "context": context,
        "question": query
    })

    answer = response.content
    logger.info("Answer generated successfully")
    return answer


if __name__ == "__main__":
    # Setup Qdrant client
    client = QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
        timeout=60.0,
    )

    query = "What was the age of Frodo in Long unexpected party?"
    results = retrieve_documents(client, query, collection_name=config.COLLECTION_NAME, k=5)

    answer = generate_answer(query=query, results=results)
    print(answer)
