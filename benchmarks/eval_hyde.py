import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import os
from app.services.vector_store import vector_store

def evaluate(use_hyde: bool):
    with open("data/eval_questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    hits = 0
    details = []
    for q in questions:
        query = q["query"]
        try:
            results = vector_store.similarity_search(query, n_results=3, use_hyde=use_hyde)
            text = " ".join(results)
            matched = [kw for kw in q["expected_keywords"] if kw in text]
            hit = len(matched) > 0
            if hit:
                hits += 1
            details.append({"query": query, "hit": hit, "matched": matched})
        except Exception as e:
            print(f"❌ {query}: {e}")
            details.append({"query": query, "hit": False, "matched": []})

    accuracy = hits / len(questions)
    return accuracy, details

if __name__ == "__main__":
    print("=" * 50)
    print("评估原始检索...")
    acc_orig, details_orig = evaluate(False)

    print("=" * 50)
    print("评估 HyDE 检索...")
    acc_hyde, details_hyde = evaluate(True)

    print("=" * 50)
    print(f"原始检索准确率: {acc_orig:.1%} ({sum(d['hit'] for d in details_orig)}/{len(details_orig)})")
    print(f"HyDE 检索准确率: {acc_hyde:.1%} ({sum(d['hit'] for d in details_hyde)}/{len(details_hyde)})")

    with open("docs/hyde_eval_result.json", "w", encoding="utf-8") as f:
        json.dump({
            "original": {"accuracy": acc_orig, "details": details_orig},
            "hyde": {"accuracy": acc_hyde, "details": details_hyde}
        }, f, ensure_ascii=False, indent=2)
    print("结果已保存: docs/hyde_eval_result.json")
