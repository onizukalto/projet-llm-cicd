from transformers import pipeline
from tools import calculator, search
from agent_v1 import CALC_PATTERN

from transformers.utils import logging
logging.set_verbosity_error()

SYSTEM_PROMPT = """Classe la question de l'utilisateur. Réponds par UN SEUL mot :
- calculator : si la question demande d'effectuer un calcul mathématique
- search : pour toute autre question

Exemples :
Question : Calcule 12 + 8
Réponse : calculator
Question : Combien font (4 + 1) * 3 ?
Réponse : calculator
Question : Quels sont les délais de livraison ?
Réponse : search
Question : Le magasin est-il ouvert 7j/7 ?
Réponse : search
Question : Quelle est la capitale de l'Italie ?
Réponse : search"""

class AgentV3:
    """Agent hybride : Qwen choisit l'outil, le code extrait et calcule."""

    def __init__(self, model="Qwen/Qwen2.5-0.5B-Instruct"):
        self.generator = pipeline("text-generation", model=model)

    def classify(self, task: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question : {task}"},
        ]
        raw = self.generator(messages, max_new_tokens=5, do_sample=False)
        text = raw[0]["generated_text"][-1]["content"].lower()
        return "calculator" if "calculator" in text else "search"

    def run(self, task: str) -> dict:
        tool = self.classify(task)

        if tool == "calculator":
            match = CALC_PATTERN.search(task)
            if match:
                try:
                    return {"answer": calculator(match.group()),
                            "tools": ["calculator"], "recovered": False}
                except ValueError:
                    return {"answer": "erreur de calcul",
                            "tools": ["calculator"], "recovered": True}
            # Qwen a dit "calcul" mais il n'y a aucune expression : on cherche
            tool = "search"

        return {"answer": search(task), "tools": ["search"], "recovered": False}

if __name__ == "__main__":
    agent = AgentV3()
    for q in ["Combien font (2 + 3) * 4 ?", "Calcule 5 * (3 + ",
              "La garantie couvre-t-elle un usage 24/7 ?", "Quelle est la couleur du ciel ?"]:
        print(q, "->", agent.run(q))