from collections import Counter
from statistics import mean
# from utils import cache
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim, dot_score, euclidean_sim, manhattan_sim
import spacy

DEF_EMB_MODEL = "thenlper/gte-large"
DEF_EMB_TYPE = "sentence_embedding"
DEF_DIST_FN = "cosine"
DEF_SPACY_LANG = "en_core_web_sm"
DEF_PREPROCESSING_ARGS = {
    "lower": True,
    "remove_punct": True,
    "remove_stopwords": True,
    "lemmatize": True,
    "dominant_k": None,
    "unique": True
}

SPACY_CACHE = {}
EMBEDDING_CACHE = {}

def is_immutable(obj):
    return isinstance(obj, (str, int, float, bool, tuple, type(None)))
def cache(cache_dict):
    def decorator_cache(func):
        def wrapper(*args, **kwargs):
            if all(is_immutable(arg) for arg in args) and all(is_immutable(val) for val in kwargs.values()):
                key = (args, frozenset(kwargs.items()))
                if key in cache_dict:
                    return cache_dict[key]
                result = func(*args, **kwargs)
                cache_dict[key] = result
            else:
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_cache

@cache(cache_dict=SPACY_CACHE)
def get_spacy_doc(text, include_syllables=False, include_constituency=False):
    spacy_engine = spacy.load(DEF_SPACY_LANG)
    return spacy_engine(text)

@cache(cache_dict=EMBEDDING_CACHE)
def get_embedding(text, model=DEF_EMB_MODEL, emb_type=DEF_EMB_TYPE):
    emb_model = SentenceTransformer(model)
    output_value = "sentence_embedding"

    if "token" in emb_type:
        output_value = "token_embeddings"

    embeddings = emb_model.encode(text, output_value=output_value)
    
    if embeddings.ndim == 2:
        embeddings = embeddings.mean(axis=0)

    return embeddings

def get_words(text, lower=True, remove_punct=True, remove_stopwords=True, lemmatize=True, unique=True, dominant_k=None):
    doc = get_spacy_doc(text)
    tokens = [token for token in doc]

    if remove_punct:
        tokens = [token for token in tokens if not token.is_punct]
    
    if remove_stopwords:
        tokens = [token for token in tokens if not token.is_stop]

    words = [token.text for token in tokens]

    if lemmatize:
        words = [token.lemma_ for token in tokens]
    
    if lower:
        words = [word.lower() for word in words]
    
    if dominant_k is None or dominant_k == 0 or dominant_k >= len(words):
        if unique:
            return list(set(words))
        return words

    word_freq = Counter(words)

    return [w[0] for w in word_freq.most_common(dominant_k)]

def compute_avg_pairwise_distances(embeddings, distance_fn=DEF_DIST_FN):
    if len(embeddings) <= 1:
        return [0]

    avg_pairwise_distances = []
    for i in range(len(embeddings)):
        pairwise_distances = []
        for j in range(len(embeddings)):
            if i != j:
                if distance_fn == "cosine":
                    distance = (1 - cos_sim(embeddings[i], embeddings[j])).item()
                elif distance_fn == "dot":
                    distance = (1 - dot_score(embeddings[i], embeddings[j])).item()
                elif distance_fn == "euclidean":
                    distance = (-euclidean_sim(embeddings[i], embeddings[j])).item()
                elif distance_fn == "manhattan":
                    distance = (-manhattan_sim(embeddings[i], embeddings[j])).item()
                else:
                    raise ValueError(f"Invalid distance function: {distance_fn}")
                pairwise_distances.append(distance)
        avg_pairwise_distances.append(mean(pairwise_distances))
    return avg_pairwise_distances

def compute_inverse_homogenization(texts, emb_model=DEF_EMB_MODEL, emb_type=DEF_EMB_TYPE,
                                   distance_fn=DEF_DIST_FN):
    def compute_text_embedding(text):
        return get_embedding(text, emb_model, emb_type)

    text_embeddings = [compute_text_embedding(text) for text in texts]
    return compute_avg_pairwise_distances(text_embeddings, distance_fn)

def compute_n_gram_diversity(text, max_n_gram=5, remove_punct=True):
    words = get_words(text, lower=True, remove_punct=remove_punct, remove_stopwords=False, lemmatize=False, unique=False)
    all_n_grams = []

    for n in range(1, max_n_gram + 1):
        all_n_grams.append([tuple(words[i:i + n]) for i in range(len(words) - n + 1)])
    
    all_n_gram_freqs = [Counter(n_grams) for n_grams in all_n_grams]
    n_gram_diversity = [len(n_gram_freqs) / len(n_grams) for n_grams, n_gram_freqs in zip(all_n_grams, all_n_gram_freqs)]

    return n_gram_diversity, all_n_gram_freqs
