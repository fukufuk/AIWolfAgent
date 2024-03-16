from time import time

from transformers import AutoModel, AutoTokenizer

start = time()

tokenizer = AutoTokenizer.from_pretrained('embedding_model')
model = AutoModel.from_pretrained('embedding_model')

print(f"Time: {time() - start}")