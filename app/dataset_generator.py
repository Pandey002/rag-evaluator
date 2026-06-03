from llama_index.core import Settings, SimpleDirectoryReader
from llama_index.core.evaluation import DatasetGenerator
from llama_index.llms.groq import Groq
from app.config import GROQ_API_KEY


def generate_dataset(docs_path: str):

    Settings.llm = Groq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile"
    )
    documents = SimpleDirectoryReader(docs_path).load_data()

    dataset_generator = DatasetGenerator.from_documents(
        documents,
        num_questions_per_chunk=1,
        show_progress=True
    )

    dataset = dataset_generator.generate_dataset_from_nodes()

    return dataset

