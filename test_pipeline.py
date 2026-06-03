from app.pipeline import build_pipeline

query_engine = build_pipeline("data/sample_docs")

response = query_engine.query("What is RAG?")

print(response)