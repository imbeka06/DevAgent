import chromadb
from chromadb.utils import embedding_functions
import os

# Point exactly to our Phase 1 database
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'vectors'))

def retrieve_code_context(query: str, n_results: int = 2):
    """
    Acts as the Repo Agent. Takes a natural language query, searches the 
    ChromaDB vector store, and returns the most relevant code snippets.
    """
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Must use the exact same embedding model we used to store the code
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    try:
        # Connect to our existing collection
        collection = client.get_collection(name="devagent_repo", embedding_function=emb_fn)
    except ValueError:
        return ["Error: 'devagent_repo' collection not found. Have you run vector_db.py yet?"]

    # Perform the vector similarity search
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if not results['documents'] or not results['documents'][0]:
        return ["No relevant code found."]

    return results['documents'][0]

# Quick test block to ensure the agent can retrieve memory
if __name__ == "__main__":
    # We ask a question about the code we indexed in Phase 1
    test_query = "What function ignores directories like node_modules and venv?"
    
    print(f"Agent Query: '{test_query}'\n")
    print("Agent Retrieving Context...\n")
    
    snippets = retrieve_code_context(test_query, n_results=1)
    
    print("-" * 40)
    print(snippets[0])
    print("-" * 40)