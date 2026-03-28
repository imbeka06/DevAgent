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
    
    # Using the exact same model string that worked perfectly in your controller
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
    response = chain.invoke({"code_structure": json.dumps(ast_analysis, indent=2)})
    
    return response.content

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from analysis.ast_parser import analyze_python_file
    
    # Target our scanner.py file
    target_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'repo_index', 'scanner.py'))
    
    print(f"Bug Hunter Target: {target_file}\n")
    ast_data = analyze_python_file(target_file)
    
    # DEBUG: Let's look at the AST data before we hand it to the AI
    print("\n DEBUG: AST Data Being Sent ")
    print(json.dumps(ast_data, indent=2))
    print("----------------------------------\n")
    
    try:
        report = hunt_for_bugs(ast_data)
        print("-" * 40)
        print("Bug Report:")
        print(report)
        print("-" * 40)
    except Exception as e:
        print(f"Error running Bug Agent: {e}")