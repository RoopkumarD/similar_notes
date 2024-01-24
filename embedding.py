import warnings

from sentence_transformers import SentenceTransformer, util
from torch import Tensor, stack

# to remove typed storage warning
warnings.filterwarnings(
    "ignore", category=UserWarning, message="TypedStorage is deprecated"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(query: list[str] | str, convert_to_tensor: bool = False):
    return model.encode(query, convert_to_tensor=convert_to_tensor)


def similarity(query: Tensor, corpus: list[Tensor]):
    t = stack(corpus)
    hits = util.semantic_search(
        query_embeddings=query,
        corpus_embeddings=t,
        top_k=5,
    )
    return hits[0]
