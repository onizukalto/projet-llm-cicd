TEST_CASES = [
    # --- 1. Cas simples ---
    {"id": "calc_01", "category": "simple",
     "task": "Calcule 25 * 4",
     "expected_answer": "100", "expected_tools": ["calculator"]},
    {"id": "calc_02", "category": "simple",
     "task": "Combien font (2 + 3) * 4 ?",
     "expected_answer": "20", "expected_tools": ["calculator"]},
    {"id": "calc_03", "category": "simple",
     "task": "Calcule 7.5 * 2",
     "expected_answer": "15", "expected_tools": ["calculator"]},
    {"id": "search_01", "category": "simple",
     "task": "Quelle est la politique de remboursement ?",
     "expected_answer": "30 jours", "expected_tools": ["search"]},
    {"id": "search_02", "category": "simple",
     "task": "LIVRAISON : combien de temps ça prend ?",
     "expected_answer": "3 à 5 jours", "expected_tools": ["search"]},

    # --- 2. Cas sans réponse ---
    {"id": "unknown_01", "category": "sans_reponse",
     "task": "Quelle est la couleur du ciel ?",
     "expected_answer": "not found", "expected_tools": ["search"]},

    # --- 3. Cas d'erreur ---
    {"id": "error_01", "category": "erreur",
     "task": "Combien font 10 / 0 ?",
     "expected_answer": "erreur", "expected_tools": ["calculator"]},
    {"id": "error_02", "category": "erreur",
     "task": "Calcule 5 * (3 + ",
     "expected_answer": "erreur", "expected_tools": ["calculator"]},

    # --- 4. Cas pièges : des chiffres dans une question qui n'est pas un calcul ---
    {"id": "trap_01", "category": "piege",
     "task": "Le remboursement est-il possible après 2-3 semaines ?",
     "expected_answer": "30 jours", "expected_tools": ["search"]},
    {"id": "trap_02", "category": "piege",
     "task": "La garantie couvre-t-elle un usage 24/7 ?",
     "expected_answer": "2 ans", "expected_tools": ["search"]},
]