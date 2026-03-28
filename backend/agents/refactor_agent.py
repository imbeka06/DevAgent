import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load the .env file
load_dotenv()

def suggest_refactor(code_string: str):
    """
    Takes raw source code and uses Gemini to suggest improvements for 
    readability, performance, and modern coding standards.
    """
    print("-> Refactor Agent: Analyzing code for structural and performance improvements...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = PromptTemplate(
        input_variables=["code"],
        template="""You are DevAgent's specialized Refactor Agent.
        Review the following Python code.
        Suggest improvements for readability, performance, PEP8 compliance, and modern Python practices (like type hinting).
        Provide the completely refactored code block at the end.

        --- Code to Refactor ---
        {code}
        ------------------------
        
        Refactoring Suggestions & Rewritten Code:"""
    )
    
    chain = prompt | llm
    response = chain.invoke({"code": code_string})
    
    return response.content

# Quick test block
if __name__ == "__main__":
    # Target  scanner.py file again
    target_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'repo_index', 'scanner.py'))
    
    print(f"Refactor Target: {target_file}\n")
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            raw_code = f.read()
            
        suggestions = suggest_refactor(raw_code)
        
        print("-" * 40)
        print("Refactor Report:")
        print(suggestions)
        print("-" * 40)
    except Exception as e:
        print(f"Error running Refactor Agent: {e}")