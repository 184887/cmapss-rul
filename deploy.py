"""Last opp appen til Hugging Face Spaces.

Krever en Hugging Face-konto og innlogging først:  uv run hf auth login
Bruk:  uv run python deploy.py <brukernavn>/<space-navn>
"""
import sys

from huggingface_hub import HfApi

# bare det appen trenger, ikke treningsdata, notebook eller .venv
FILER = [
    "app.py",
    "requirements.txt",
    "README.md",
    "cmapss/*.py",
    "models/rul_modell.joblib",
    "data/raw/test_FD001.txt",
    "eksempeldata/*.txt",
]

space = sys.argv[1]
api = HfApi()
api.create_repo(space, repo_type="space", space_sdk="gradio", exist_ok=True)
api.upload_folder(folder_path=".", repo_id=space, repo_type="space", allow_patterns=FILER)
print(f"Ferdig: https://huggingface.co/spaces/{space}")
