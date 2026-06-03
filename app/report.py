def generate_report(results):
    total = len(results)
    faithful_count = sum(1 for r in results if r["faithfulness"])
    relevant_count = sum(1 for r in results if r["relevancy"])
    
    faithfulness_score = round((faithful_count / total) * 100, 2)
    relevancy_score = round((relevant_count / total) * 100, 2)
    overall_score = round((faithfulness_score + relevancy_score) / 2, 2)
    report = {
            "total_questions": total,
            "faithfulness_score": f"{faithfulness_score}%",
            "relevancy_score": f"{relevancy_score}%",
            "overall_score": f"{overall_score}%",
            "details": results
        }
    return report