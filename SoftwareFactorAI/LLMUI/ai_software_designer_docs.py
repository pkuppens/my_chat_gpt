import sys
from typing import Optional
from utils.ai_doc_writer import main as ai_doc_writer_main

def main(file_path: Optional[str] = None) -> int:
    """
    Main function to read JSON, process items, and write content to files.
    
    Args:
        file_path: Path to the JSON file (optional, defaults to command line arg)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    return ai_doc_writer_main(file_path or sys.argv[1] or 'ai_software_designer_docs.json')

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
