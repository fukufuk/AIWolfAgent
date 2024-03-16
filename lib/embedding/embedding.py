import pickle

import torch
from torch import Tensor
from torch.nn.functional import cosine_similarity
from transformers import AutoModel, AutoTokenizer


class Embedding:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('embedding_model')
        self.model = AutoModel.from_pretrained('embedding_model')
        with open("lib/embedding/data/script_emb.pickle", "rb") as f:
            self.ex_scripts = pickle.load(f)

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
        return embeddings.unsqueeze(0)

    def check_role_suspicion(self, text: str) -> str:
        txt_emb = self.encode(text)
        sim = cosine_similarity(torch.cat(self.ex_scripts[1]),
                                txt_emb,
                                dim=2)
        max_index = max(enumerate(sim.tolist()), key=lambda x: x[1])[0]
        if sim[max_index].item() < 0.91:
            return None
        return self.ex_scripts[0][max_index]


def _average_pool(last_hidden_states: Tensor, attention_mask: Tensor
                  ) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(
        ~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
