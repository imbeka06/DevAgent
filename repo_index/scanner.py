import os

# Folders I do not want the AI to waste time reading
IGNORE_DIRS = {'.git', 'venv', 'node_modules', '__pycache__', 'database'}
# File types the AI should care about
SUPPORTED_EXTENSIONS = {'.py', '.ts', '.js', '.md', '.json'}

def scan_repository(repo_path: str):
    """
    Crawls a local directory and extracts the text from code files.
    Returns a list of dictionaries containing file metadata and content.
    """
    scanned_files = []

    for root, dirs, files in os.walk(repo_path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            # Check if the file ends with a supported extension
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Only add files that actually have content
                        if content.strip():
                            scanned_files.append({
                                "metadata": {"file_path": file_path},
                                "content": content
                            })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return scanned_files

# Quick test block to ensure it works locally
if __name__ == "__main__":
    # Test by scanning the current DevAgent directory
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    results = scan_repository(current_dir)
    print(f"Scanned {len(results)} files.")
    for res in results:
        print(f"- {res['metadata']['file_path']}")