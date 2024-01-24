import pickle
from time import time

import torch
from lib import util
from lib.embedding import Embedding
from torch.nn.functional import cosine_similarity

texts = ["私はAgent[01]のことを本物の占い師だと信じていません！", "私はAgent[02]のことを本物の占い師だと信じていません！", "私はAgent[03]のことを本物の占い師だと信じていません！"]
embedding = Embedding()
start = time()
suspects = util.map_async(
    func=embedding.check_role_suspicion,
    data=texts,
    limit=8
)
end = time()
print(suspects)
print(end - start)
start = time()
suspects = []
for t in texts:
    tx = embedding.check_role_suspicion(t)
    suspects.append(tx)
end = time()
print(suspects)
print(end - start)


# with open('lib/embedding/data/script_emb.pickle', 'rb') as f:
#     script = pickle.load(f)

# start = time()
# emb = embedding.encode("私はAgent[01]のことを本物の占い師だと信じていません！")
# end = time()
# print(end - start)

# sim = cosine_similarity(torch.cat(script[1]),
#                         emb,
#                         dim=2)
# max_index = max(enumerate(sim.tolist()), key=lambda x: x[1])[0]

# print(sim[max_index].item())
# print(script[0][max_index])

# with open('lib/embedding/data/script.pickle', 'rb') as f:
#     script = pickle.load(f)

# script_embedding = map(embedding.encode, script)
# script_embedding = list(script_embedding)

# with open('lib/embedding/data/script_emb.pickle', 'wb') as f:
#     pickle.dump([script, script_embedding], f)

# print(len(script))
# print(len(script_embedding))
