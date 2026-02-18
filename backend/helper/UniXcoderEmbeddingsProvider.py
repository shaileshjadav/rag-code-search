from abc import abstractmethod
from typing import Union, List, Optional

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel

import numpy as np
import torch
import re

from backend.model.unixcoder import UniXcoder

class BaseEmbeddingsProvider:

    @abstractmethod
    def embed_code(
            self, code: Optional[str] = None, docstring: Optional[str] = None
    ) -> np.array:
        """Converts code and/or docstring to vector"""

class UniXcoderEmbeddingsProvider(BaseEmbeddingsProvider):
    def __init__(self, device: Optional[str] = None):
        default_device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(default_device if device is None else device)
        self.model = UniXcoder("microsoft/unixcoder-base")
        self.model.to(self.device)
        self.model_name = "microsoft/unixcoder-base"

    def embed_code(
        self, code: Optional[str] = None, docstring: Optional[str] = None
    ) -> np.array:
        tokens_ids = self.model.tokenize(
            [f"{docstring or ''} {code or ''}"], max_length=512, mode="<encoder-only>"
        )
        source_ids = torch.tensor(tokens_ids).to(self.device)
        _, func_embedding = self.model(source_ids)
        vector = func_embedding.detach().cpu().numpy()[0]
        return vector