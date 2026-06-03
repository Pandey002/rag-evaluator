from app.pipeline import build_pipeline
from app.dataset_generator import generate_dataset
from app.evaluator import evaluate_pipeline
from app.report import generate_report

query_engine = build_pipeline("data/sample_docs")
dataset = generate_dataset("data/sample_docs")
questions = list(dataset.queries.values())

results = evaluate_pipeline(query_engine, questions)
report = generate_report(results)

print("===== RAG EVALUATION REPORT =====")
print("Total Questions:", report["total_questions"])
print("Faithfulness Score:", report["faithfulness_score"])
print("Relevancy Score:", report["relevancy_score"])
print("Overall Score:", report["overall_score"])