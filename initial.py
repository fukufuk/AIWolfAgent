import pickle

from huggingface_hub import snapshot_download
from lib.embedding.embedding import Embedding

if __name__ == "__main__":
    # Download the model from the Hugging Face Hub
    snapshot_download(repo_id="intfloat/multilingual-e5-large",
                      local_dir="embedding_model")
