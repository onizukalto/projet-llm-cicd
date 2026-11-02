import argparse
import json
import sys
from evaluate import evaluate
from agent_v1 import AgentV1

# Seuils de qualité. En dessous, la CI échoue.
THRESHOLDS = {
    "task_score_min": 0.75,        # part minimale de bonnes réponses
    "category_min": {"erreur": 1.0},  # les erreurs doivent TOUJOURS être gérées
}


def check(df):
    failures = []
    task = df.task_score.mean()
    if task < THRESHOLDS["task_score_min"]:
        failures.append(f"task_score {task:.2f} < {THRESHOLDS['task_score_min']}")
    by_cat = df.groupby("category").task_score.mean()
    for cat, minimum in THRESHOLDS["category_min"].items():
        if by_cat.get(cat, 0) < minimum:
            failures.append(f"catégorie '{cat}' {by_cat.get(cat, 0):.2f} < {minimum}")
    if df.error.any():
        failures.append(f"{int(df.error.sum())} appels ont planté")
    return task, by_cat, failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=["v1", "v3"], default="v1")
    args = parser.parse_args()

    if args.agent == "v1":
        agent = AgentV1()
    else:
        from agent_v3 import AgentV3
        agent = AgentV3()

    df = evaluate(agent, args.agent, repetitions=1)
    task, by_cat, failures = check(df)

    report = {"agent": args.agent, "task_score": round(task, 3),
              "by_category": by_cat.round(3).to_dict(), "failures": failures}
    with open(f"eval_report_{args.agent}.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if failures:
        print("\nÉCHEC du contrôle qualité")
        sys.exit(1)
    print("\nContrôle qualité réussi")