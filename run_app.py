import subprocess
import sys

def run_script(script_name, args=None):
    """
    Runs a Python script using the current interpreter.
    
    Args:
        script_name (str): The filename of the script to run.
        args (list, optional): A list of command-line arguments to pass.
    """
    command = [sys.executable, script_name]
    if args:
        command.extend(args)
    
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)

def main():
    try:
        # Step 0: Install/Update Requirements
        print("Step 0: Running 00_requirements.py to install/update dependencies...")
        run_script("00_run_requirements.py")
        
        # Step 1: Document Ingestion
        print("Step 1: Running ingest.py to ingest documents...")
        run_script("ingest.py")
        
        # Step 2: Indexing Documents
        print("Step 2: Running 02_index_documents.py to build the FAISS index...")
        run_script("02_index_documents.py")
        
        # Step 3: Test Prompting (optional)
        print("Step 3: Running prompting.py to test the Q&A pipeline...")
        run_script("prompting.py")
        
        # Step 4: Launch the Streamlit Interface
        print("Step 4: Launching the Streamlit interface (04_interface.py)...")
        # This command will open a new window/tab (or display on your codespace/web browser) with the interface.
        subprocess.run(["streamlit", "run", "04_interface.py"], check=True)
    
    except subprocess.CalledProcessError as error:
        print(f"An error occurred while running the pipeline: {error}")
        sys.exit(error.returncode)

if __name__ == "__main__":
    main()
