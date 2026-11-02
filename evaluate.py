import time
import pandas as pd
from eval_cases import TEST_CASES
from agent_v1 import AgentV1
from agent_v3 import AgentV3


def evaluate(agent, version, repetitions=3):
    results = []

    for case in TEST_CASES:
        for run in range(repetitions):
            start = time.perf_counter()

            try:
                output = agent.run(case["task"])
                error = False
            except Exception:
                output = {"answer": "", "tools": [], "recovered": False}
                error = True

            latency = time.perf_counter() - start

            answer = output["answer"].lower()

            task_score = float(case["expected_answer"].lower() in answer)
            tool_score = float(output["tools"] == case["expected_tools"])


            results.append({
                "version": version,
                "case_id": case["id"],
                "category": case["category"],
                "run": run + 1,
                "task_score": task_score,
                "tool_score": tool_score,
                "latency_s": latency,
                "error": error,
                "answer": answer,
            })

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = pd.concat([
        evaluate(AgentV1(), "v1"),
        evaluate(AgentV3(), "v3"),
        evaluate(AgentV3(model="Qwen/Qwen2.5-1.5B-Instruct"), "v3-1.5B"),
    ])
    df.to_csv("results.csv", index=False)

    print("Scores par version et catégorie :")
    print(df.groupby(["version", "category"])[["task_score", "tool_score"]].mean())

    print("\nRésumé par version :")
    print(df.groupby("version").agg(
        task=("task_score", "mean"),
        tools=("tool_score", "mean"),
        latence_moy=("latency_s", "mean"),
        erreurs=("error", "mean"),
    ).round(3))

