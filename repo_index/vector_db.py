import os
import chromadb
from chromadb.utils import embedding_functions

# Ensure the database goes to the exact folder I created
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'vectors'))

def get_db_client():
    """Initializes and returns the local ChromaDB client."""
    return chromadb.PersistentClient(path=DB_PATH)

def store_code_embeddings(scanned_files):
    """
    Takes scanned files, converts them to vector embeddings,
    and stores them in ChromaDB for AI retrieval.
    """
    client = get_db_client()
    
    # Using a fast, local embedding model (no API keys, processes 100% locally)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Create or connect to the collection (like a table in SQL)
    collection = client.get_or_create_collection(name="devagent_repo", embedding_function=emb_fn)
    
    if not scanned_files:
        print("No files provided to index.")
        return

    ids = []
    documents = []
    metadatas = []

    for i, file_data in enumerate(scanned_files):
        # Generate a unique ID for the vector
        file_name = os.path.basename(file_data['metadata']['file_path'])
        doc_id = f"file_{i}_{file_name}"
        
        ids.append(doc_id)
        documents.append(file_data["content"])
        metadatas.append(file_data["metadata"])

    # Push to the database
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Successfully embedded and stored {len(scanned_files)} files in ChromaDB.")

# Quick test block
if __name__ == "__main__":
    from scanner import scan_repository
    
    print("1. Scanning repository...")
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    files = scan_repository(current_dir)
    
    print("2. Storing embeddings in ChromaDB (this will download the embedding model the first time)...")
    store_code_embeddings(files)