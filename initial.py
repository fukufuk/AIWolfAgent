import pickle

from huggingface_hub import snapshot_download
from lib.embedding.embedding import Embedding

if __name__ == "__main__":
    # Download the model from the Hugging Face Hub
    snapshot_download(repo_id="intfloat/multilingual-e5-large",
                      local_dir="embedding_model")
    
    # 類似度検索をするためのデータ生成
    embedding = Embedding()
    players = ["私", "Agent[01]", "Agent[02]", "Agent[03]", "Agent[04]", "Agent[05]"]
    roles = ["人狼", "村人", "狂人", "占い師", "白", "黒"]
    txts = ["{}は{}だ", "{}は{}ではない"]
    examples = []
    for txt in txts:
        for a in players:
            for b in roles:
                examples.append(txt.format(a, b))
    script_embedding = map(embedding.encode, examples)
    script_embedding = list(script_embedding)

    with open('lib/embedding/data/script_emb.pickle', 'wb') as f:
        pickle.dump([examples, script_embedding], f)
