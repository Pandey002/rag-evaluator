from llama_index.core import Settings
from llama_index.core.evaluation import (FaithfulnessEvaluator,RelevancyEvaluator)
from llama_index.llms.groq import Groq

from app.config import GROQ_API_KEY


def evaluate_pipeline(query_engine, questions):
    
    Settings.llm = Groq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile"
    )
    faithfulness_evaluator = FaithfulnessEvaluator()
    relevancy_evaluator = RelevancyEvaluator()
    
    results = []
    
    for question in questions:
        response = query_engine.query(question)
        
        faithfulness_result = faithfulness_evaluator.evaluate_response(response=response)
        relevancy_result = relevancy_evaluator.evaluate_response(query=question, response=response)
        
        results.append({
            "question": question,
            "response": response,
            "faithfulness": faithfulness_result.passing,
            "relevancy": relevancy_result.passing
        })
        
    return results
        
    