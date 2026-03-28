import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load the .env file
load_dotenv()

def hunt_for_bugs(ast_analysis: dict):
    """
    Takes the structured AST representation of a file and uses Gemini 
    to identify logical flaws, missing error handling, or security risks.
    """
    print("-> Bug Agent: Analyzing code structure for vulnerabilities...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = PromptTemplate(
        input_variables=["code_structure"],
        template="""You are DevAgent's specialized Bug Hunter.
        Review the following Python file structure (extracted via AST).
        Identify any potential bugs, missing error handling, or poor practices in the functions.
        Be direct and provide specific code fixes.
        If the code looks perfect, say "No critical vulnerabilities detected."

        --- Code Structure ---
        {code_structure}
        ----------------------
        
        Bug Report:"""
    )
    
    chain = prompt | llm
    # Convert the Python dictionary to a readable JSON string for the AI
    response = chain.invoke({"code_structure": json.dumps(ast_analysis, indent=2)})
    
    return response.content

# Quick test block
if __name__ == "__main__":
    # Import  AST parser from Phase 1 to feed the Bug Agent
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from analysis.ast_parser import analyze_python_file
    
    # Analyze  scanner.py file
    target_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'repo_index', 'scanner.py'))
    ast_data = analyze_python_file(target_file)
    
    print(f"Bug Hunter Target: {target_file}\n")
    
    try:
        report = hunt_for_bugs(ast_data)
        print("-" * 40)
        print(report)
        print("-" * 40)
    except Exception as e:
        print(f"Error running Bug Agent: {e}")