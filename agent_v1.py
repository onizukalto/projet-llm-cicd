import re
from tools import calculator, search

# Chiffres, opérateurs, points, parenthèses et espaces, contenant au moins un opérateur
CALC_PATTERN = re.compile(r"[0-9().\s]*\d[0-9().\s]*[+\-*/][0-9+\-*/().\s]*")

class AgentV1:
    """Agent à base de règles : aucune IA, choix d'outil par motif."""

    def run(self, task: str) -> dict:
        match = CALC_PATTERN.search(task)

        if match:
            tool = "calculator"
            try:
                answer = calculator(match.group())
                recovered = False
            except ValueError:
                answer = "erreur de calcul"
                recovered = True
        else:
            tool = "search"
            answer = search(task)
            recovered = False

        return {"answer": answer, "tools": [tool], "recovered": recovered}

if __name__ == "__main__":
    agent = AgentV1()
    for q in ["Calcule 25 * 4", "Quelle est la politique de remboursement ?",
              "Combien font 10 / 0 ?", "Quelle est la couleur du ciel ?"]:
        print(q, "->", agent.run(q))