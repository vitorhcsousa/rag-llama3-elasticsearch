import json
from llama_index.core import Document
from elasticsearch import AsyncElasticsearch
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

# Elasticsearch client setup
es_client = AsyncElasticsearch("http://localhost:9200")

es_vector_store = ElasticsearchStore(
    index_name="calls",
    vector_field='conversation_vector',
    text_field='conversation',
    es_client=es_client  # Pass the local client instead of cloud credentials
)


def get_documents_from_file(file_path) -> list:
    """
    This function reads a json file and returns a list of documents
    """
    with open(file_path, mode="rt") as f:
        conversation_dict = json.loads(f.read())
    documents = [Document(text=item["conversation"], metadata={"conversation_id": item["conversation_id"]}) for item in
                 conversation_dict]
    return documents


def ingest_documents(documents):
    ollama_embedding = OllamaEmbedding("llama3")
    pipeline = IngestionPipeline(transformations=[SentenceSplitter(chunk_size=350, chunk_overlap=50), ollama_embedding],
                                 vector_store=es_vector_store)
    pipeline.run(documents=documents)
    print("Pipeline run completed")
