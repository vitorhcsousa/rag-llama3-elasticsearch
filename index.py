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


def get_documents_from_json(json_data) -> list:
    """
    This function receives a JSON object (Python dictionary) and returns a list of documents.
    """
    documents = [Document(text=item["conversation"], metadata={"conversation_id": item["conversation_id"]})
                 for item in json_data]
    return documents


def ingest_documents(documents):
    """
    This function ingests the documents into Elasticsearch
    """
    # TODO make the model a parameter from the interface
    ollama_embedding = OllamaEmbedding("llama3")
    pipeline = IngestionPipeline(transformations=[SentenceSplitter(chunk_size=350, chunk_overlap=50), ollama_embedding],
                                 vector_store=es_vector_store)
    pipeline.run(documents=documents)
    print("Pipeline run completed")
