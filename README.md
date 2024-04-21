# RAG with LlamaIndex, Elasticsearch and Llama3 🦙
![Llama](assets/llamma.jpeg)

This repository houses a powerful tool that blends **Streamlit**, **Elasticsearch**, and cutting-edge language models like **Llama3**. It's designed to simplify querying documents via conversation vectors embedded into a dynamic, user-friendly web interface.

## Features 🌟

- **Document Upload:** Upload JSON files with ease.
- **Efficient Search:** Powered by Elasticsearch.
- **Natural Language Queries:** Harness models like Llama3 to query using everyday language.
- **Interactive UI:** Real-time updates and feedback.
- **Scalable:** Built to manage extensive data volumes and complex queries.

## Getting Started 🚀

### Prerequisites

- Python 3.8+
- Elasticsearch 7.x+
- Ollama
- llama_index
- Streamlit
- poetry

### Installation

Clone and set up the project:

```bash
git clone https://github.com/vitorhcsousa/rag-llama3-elasticsearch.git
cd rag-llama3-elasticsearch
poetry install
```

### Usage
Launch the app:

```bash
poetry run streamlit run app.py
```

### Structure 📂
- app.py: The Streamlit application entry point.
- index.py: Handles document indexing in Elasticsearch.
- query.py: Manages the query engine setup and execution.
- assets/: Static files like images for the UI.

### Contributing 🤝
Interested in contributing? Great! Here's how:

1. Fork the repo.
2. Create your feature branch (git checkout -b feature-branch).
3. Commit your changes (git commit -am 'Add some feature').
4. Push to the branch (git push origin feature-branch).
5. Create a new Pull Request.