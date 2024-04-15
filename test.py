from time import time

from lib.embedding import Embedding

embedder = Embedding()

start = time()
emb = embedder.encode("I am a villager")
print("time:", time() - start)

print(len(emb))
print(len(emb[0]))
print(len(embedder.df_scripts.iloc[0]['emb']))
