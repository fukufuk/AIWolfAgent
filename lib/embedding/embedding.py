import pickle

import numpy as np
from datasets import load_dataset
from numpy import dot
from numpy.linalg import norm
from torch import Tensor
from transformers import AutoModel, AutoTokenizer


class Embedding:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('embedding_model')
        self.model = AutoModel.from_pretrained('embedding_model')
        self.df_scripts = load_dataset(
            "fukufuk/aiwolf-convs",
            split="train").to_pandas()

    def encode(self, text: str) -> Tensor:
        batch_dict = self.tokenizer(
            [text],
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors="pt")
        outputs = self.model(**batch_dict)
        embeddings = _average_pool(
            outputs.last_hidden_state,
            batch_dict["attention_mask"])
        return embeddings.tolist()

    def check_role_suspicion(self, text: str) -> str:
        txt_emb = self.encode(text)
        df = self.df_scripts.copy(deep=True)
        df["sim"] = df["emb"].apply(_add_sim, txt_emb=txt_emb)
        max_index = df.sort_values('sim', ascending=False).iloc[0]
        print("Embeddingの結果:", text, df.sort_values('sim', ascending=False).head(3))
        if max_index['sim'] < 0.94:
            return None
        return max_index['summary']


def _average_pool(last_hidden_states: Tensor, attention_mask: Tensor
                  ) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(
        ~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def _cosine_similarity(v1: list, v2: list) -> float:
    v1 = np.array([v1])
    v2 = np.array(v2).T
    return dot(v1, v2) / (norm(v1) * norm(v2))


def _add_sim(ex_emb: list, txt_emb: list) -> float:
    return _cosine_similarity(ex_emb, txt_emb)
