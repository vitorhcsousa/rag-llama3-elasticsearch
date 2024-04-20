import streamlit as st
from PIL import Image
import asyncio
from elasticsearch import AsyncElasticsearch
from index import get_documents_from_file, ingest_documents
from query import setup_query_engine, execute_query
import time
# Streamlit page configuration
st.set_page_config(page_title="Document Query Interface", layout="wide")

async def check_embeddings():
    es_client = AsyncElasticsearch("http://localhost:9200")
    index_info = await es_client.indices.exists(index="calls")
    if index_info:
        doc_count = await es_client.count(index="calls", body={"query": {"exists": {"field": "conversation_vector"}}})
        embeddings_present = doc_count['count'] > 0
    else:
        embeddings_present = False
    return embeddings_present

def main():
    banner = Image.open('assets/img_1.png')
    st.markdown("<h1 style='text-align: center; color: #01bfaa;'>RAG with Elasticsearch and Llama3 Hands-On</h1>", unsafe_allow_html=True)

    st.sidebar.image(banner)
    st.markdown("<h2 style='text-align: center; color: #e16217;'>Select the Model</h2>", unsafe_allow_html=True)
    model_name = st.selectbox("", ["llama3", "llama2", "mistral"], index=0)
    st.markdown("<h2 style='text-align: center; color: #fb9b43;'>Load the Documents</h2>", unsafe_allow_html=True)

    embeddings_present = asyncio.run(check_embeddings())

    json_file = None
    if not embeddings_present:
        json_file = st.file_uploader("Upload a JSON file with conversations", type=['json'])
        if json_file is not None:
            documents = get_documents_from_file(json_file)
            ingest_documents(documents)
    else:
        st.success("Embeddings are already present in Elasticsearch.")

    st.markdown("<h2 style='text-align: center; color: #ffe79c;'>Enter your query</h2>", unsafe_allow_html=True)

    query_text = st.text_input("", "Give me a summary of water related issues")

    if st.button('Run Query'):
        query_engine = setup_query_engine(model_name)
        start_time = time.time()
        result = execute_query(query_engine, query_text)

        end_time = time.time()

        execution_time = round(end_time - start_time, 2)
        st.write(result.response if result else "No results found.")
        st.write(f"Query executed in {execution_time} seconds")
    st.markdown("""
    <br> <br>
    <br> <br>
    <br> <br>
    <br> <br>
    <br>
        <footer style='text-align: center; color: grey; padding: 10px; background-color: #f5f5f5;'>
            © 2024 Vitor Sousa.
        </footer>
        """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
