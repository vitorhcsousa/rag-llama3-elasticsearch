from llama_index.core import VectorStoreIndex, QueryBundle, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from index import es_vector_store


def setup_query_engine(model_name="llama3"):
    local_llm = Ollama(model=model_name)
    Settings.embed_model = OllamaEmbedding(model_name)
    index = VectorStoreIndex.from_vector_store(es_vector_store)
    return index.as_query_engine(local_llm, similarity_top_k=10)


def execute_query(query_engine, query_text):
    bundle = QueryBundle(query_text, embedding=Settings.embed_model.get_query_embedding(query_text))
    result = query_engine.query(bundle)
    return result
