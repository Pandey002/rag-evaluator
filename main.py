import nest_asyncio
import streamlit as st

from app.dataset_generator import generate_dataset
from app.evaluator import evaluate_pipeline
from app.pipeline import build_pipeline
from app.report import generate_report

nest_asyncio.apply()

st.set_page_config(page_title="RAG Evaluator", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e2e8f0;
}

.main { background-color: #0a0a0f; padding: 2rem; }

.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00ff87, #0096ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}

.hero-sub {
    color: #64748b;
    font-size: 1rem;
    font-weight: 300;
    margin-bottom: 2rem;
}

.metric-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    text-align: center;
}

.metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #00ff87;
}

.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: #0096ff;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 2rem 0 1rem 0;
    border-left: 3px solid #0096ff;
    padding-left: 0.75rem;
}

.question-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
}

.question-text {
    font-size: 0.95rem;
    color: #cbd5e1;
    margin-bottom: 0.75rem;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-right: 0.4rem;
}

.badge-pass { background: #052e16; color: #00ff87; border: 1px solid #00ff87; }
.badge-fail { background: #2d0a0a; color: #ff4d4d; border: 1px solid #ff4d4d; }

.run-btn > button {
    background: linear-gradient(135deg, #00ff87, #0096ff) !important;
    color: #0a0a0f !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    letter-spacing: 0.05em !important;
}

.divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">RAG Pipeline Evaluator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Benchmark your retrieval pipeline with automated faithfulness and relevancy scoring.</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Upload Documents</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload your documents (.txt or .pdf)",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

docs_path = "data/sample_docs"

if uploaded_files:
    import os
    import shutil
    save_dir = "data/uploaded_docs"
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    os.makedirs(save_dir, exist_ok=True)
    for file in uploaded_files:
        with open(os.path.join(save_dir, file.name), "wb") as f:
            f.write(file.read())
    docs_path = save_dir
    
st.markdown('<div class="run-btn">', unsafe_allow_html=True)
run = st.button("▶ Run Evaluation")
st.markdown('</div>', unsafe_allow_html=True)

if run:
    with st.spinner("Building pipeline..."):
        query_engine = build_pipeline(docs_path)

    with st.spinner("Generating questions from documents..."):
        dataset = generate_dataset(docs_path)
        questions = [q for q in list(dataset.queries.values()) if q.strip().endswith("?")][:10]

    with st.spinner("Evaluating pipeline..."):
        results = evaluate_pipeline(query_engine, questions)

    report = generate_report(results)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Overall Scores</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Faithfulness</div>
            <div class="metric-value">{report["faithfulness_score"]}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Relevancy</div>
            <div class="metric-value">{report["relevancy_score"]}</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Score</div>
            <div class="metric-value">{report["overall_score"]}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Question Breakdown</div>', unsafe_allow_html=True)

    for r in report["details"]:
        faith_badge = '<span class="badge badge-pass">✓ Faithful</span>' if r["faithfulness"] else '<span class="badge badge-fail">✗ Unfaithful</span>'
        rel_badge = '<span class="badge badge-pass">✓ Relevant</span>' if r["relevancy"] else '<span class="badge badge-fail">✗ Not Relevant</span>'

        st.markdown(f"""
        <div class="question-card">
            <div class="question-text">Q: {r["question"]}</div>
            {faith_badge}{rel_badge}
        </div>""", unsafe_allow_html=True)