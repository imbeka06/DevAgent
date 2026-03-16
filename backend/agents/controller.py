import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Import our repo_agent to get the code context
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.agents.repo_agent import retrieve_code_context

# Load the .env file so we can securely access the API key
load_dotenv()

def get_llm():
    """Initializes the LLM using Google's Gemini API."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in .env file.")
    
    # Using gemini-1.5-flash for speed and efficiency.
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def orchestrate_query(query: str):
    """
    The main brain of DevAgent. 
    1. Gets context from the vector database.
    2. Packages it into a prompt.
    3. Asks the LLM to analyze it.
    """
    print("-> Controller: Searching vector memory for context...")
    
    # Grab the raw code as a string
    context_results = retrieve_code_context(query, n_results=1)
    context = context_results[0] if isinstance(context_results, list) else context_results

    if "No relevant code found" in context or "Error" in context:
        context = "No relevant codebase context found for this query."

    print("-> Controller: Context retrieved. Handing to Gemini...\n")
    
    llm = get_llm()
    
    # Instruct the AI on how to behave using langchain_core
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="""You are DevAgent, an expert AI software engineer.
        Use the following code context retrieved from the user's repository to answer their question.
        Be concise, accurate, and provide code snippets if necessary.
        If the answer cannot be determined from the context, state that clearly.

        --- Code Context ---
        {context}
        --------------------

        Developer Question: {query}
        
        DevAgent Response:"""
    )
    
    # Modern LangChain Expression Language (LCEL) syntax
    chain = prompt | llm
    response = chain.invoke({"context": context, "query": query})
    
    return response.content

# Quick test block
if __name__ == "__main__":
    test_question = "Explain how the scan_repository function works and what folders it ignores."
    
    print(f"User: {test_question}\n")
    try:
        final_answer = orchestrate_query(test_question)
        print("-" * 40)
        print("DevAgent (Powered by Gemini):")
        print(final_answer)
        print("-" * 40)
    except Exception as e:
        print(f"\nSystem Error: {e}")