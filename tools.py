import re

KNOWLEDGE_BASE = {
    "remboursement": "Les remboursements sont possibles sous 30 jours.",
    "livraison": "La livraison prend 3 à 5 jours ouvrés.",
    "garantie": "La garantie couvre 2 ans.",
}

# Seuls les chiffres, espaces, opérateurs, points et parenthèses sont autorisés
ALLOWED = re.compile(r".+")

def calculator(expression: str) -> str:
    """Calcule une expression simple, ex : '25 * 4'."""
    expression = expression.strip()
    if not expression or not ALLOWED.match(expression):
        raise ValueError(f"Expression invalide : {expression!r}")

    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        raise ValueError(f"Calcul impossible : {expression!r}") from e

    # 100.0 -> "100", 2.5 -> "2.5"
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return str(result)

def search(query: str) -> str:
    """Cherche un mot-clé de la base dans la requête."""
    query = query.lower()
    for keyword, answer in KNOWLEDGE_BASE.items():
        if keyword in query:
            return answer
    return "not found"

if __name__ == "__main__":
    print(calculator("25 * 4"))
    print(search("Quelle est la politique de remboursement ?"))
    print(search("Quelle est la couleur du ciel ?"))
    try:
        calculator("import os")
    except ValueError as e:
        print("Erreur attendue :", e)