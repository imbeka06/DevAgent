import ast
import os
import json

def analyze_python_file(file_path: str):
    """
    Reads a Python file and returns a structured dictionary of its 
    classes, functions, arguments, and docstrings.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

    try:
        # This builds the Abstract Syntax Tree
        tree = ast.parse(file_content)
    except SyntaxError as e:
        return {"error": f"Syntax error in code: {e}"}

    analysis = {
        "file": os.path.basename(file_path),
        "classes": [],
        "functions": []
    }

    # Walk through the tree to find classes and functions
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "methods": []
            }
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    class_info["methods"].append(child.name)
            analysis["classes"].append(class_info)

        elif isinstance(node, ast.FunctionDef):
            func_info = {
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "args": [arg.arg for arg in node.args.args]
            }
            analysis["functions"].append(func_info)

    return analysis

# Quick test block
if __name__ == "__main__":
    #  test by analyzing the scanner.py file I wrote 
    test_target = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'repo_index', 'scanner.py'))
    
    print(f"Analyzing: {test_target}\n")
    result = analyze_python_file(test_target)
    
    # Print the output 
    print(json.dumps(result, indent=2))