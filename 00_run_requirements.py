# 00_run_requirements.py
import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def install_requirements():
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        logging.error(f"{req_file} not found. Please ensure it exists in the project root.")
        sys.exit(1)
    
    logging.info("Checking pip availability...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        logging.error("pip is not installed or not available. Please install pip and try again.")
        sys.exit(1)

    logging.info("Installing required packages from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        logging.info("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred during installation of packages: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()