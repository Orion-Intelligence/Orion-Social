import asyncio
import numpy as np
from typing import List
from pathlib import Path
from sentence_transformers import SentenceTransformer

class nlp_semantic_service:
    def __init__(self):
        self._model = None
        self._model_name = "BAAI/bge-small-en-v1.5"
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self._model_path = base_dir / "raw" / "model" / "semantic"
        self._load_model_sync()

    def _load_model_sync(self):
        if self._model is None:
            self._model = SentenceTransformer(str(self._model_path))

    def _encode_sync(self, data: List[str], normalize: bool = True) -> List[List[float]]:
        data = [t[:2500] for t in data]
        vecs = self._model.encode(data, normalize_embeddings=normalize, convert_to_numpy=True)
        return np.asarray(vecs, dtype=np.float32).tolist()

    async def parse(self, data: List[str]) -> dict:
        result = await asyncio.to_thread(self._encode_sync, data, True)
        dim = len(result[0]) if result else 0
        return {"model": self._model_name, "embeddings": result, "dim": dim}
