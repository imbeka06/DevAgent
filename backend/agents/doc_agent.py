import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load the .env file
load_dotenv()

def generate_documentation(code_string: str):
    """
    Takes raw source code and uses Gemini to generate a clean, 
    Markdown-formatted technical documentation block.
    """
    print("Doc Agent: Generating technical documentation for the code...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = PromptTemplate(
        input_variables=["code"],
        template="""You are DevAgent's specialized Technical Writer.
        Read the following Python code and generate a clean, professional Markdown documentation file for it.
        Include:
        - A brief overview of what the code does.
        - Detailed explanations of the primary functions or classes.
        - An 'Example Usage' section showing how another developer would call this code.

        --- Source Code ---
        {code}
        -------------------
        
        Markdown Documentation:"""
    )
    
    chain = prompt | llm
    response = chain.invoke({"code": code_string})
    
    return response.content

# Quick test block
if __name__ == "__main__":
    # Target our scanner.py file one last time
    target_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'repo_index', 'scanner.py'))
    
    print(f"Documentation Target: {target_file}\n")
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            raw_code = f.read()
            
        docs = generate_documentation(raw_code)
        
        print("-" * 40)
        print("Generated Documentation:\n")
        print(docs)
        print("-" * 40)
    except Exception as e:
        print(f"Error running Doc Agent: {e}")