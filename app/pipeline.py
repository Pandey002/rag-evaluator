import chromadb
from llama_index.core import (Settings, SimpleDirectoryReader, StorageContext,VectorStoreIndex)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from app.config import GROQ_API_KEY
from llama_index.vector_stores.chroma import ChromaVectorStore



def build_pipeline(docs_path: str):

    Settings.llm = Groq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile"
    )
    
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    
    documents = SimpleDirectoryReader(docs_path).load_data()

    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.get_or_create_collection("rag_eval")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    query_engine = index.as_query_engine()

    return query_engine

