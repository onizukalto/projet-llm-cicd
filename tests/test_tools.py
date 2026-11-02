import pytest
from tools import calculator, search
from agent_v1 import AgentV1


# --- calculator ---
@pytest.mark.parametrize("expr,expected", [
    ("25 * 4", "100"),
    ("(2 + 3) * 4", "20"),
    ("7.5 * 2", "15"),     # 15.0 doit devenir "15"
    ("10 / 4", "2.5"),
])
def test_calculator_results(expr, expected):
    assert calculator(expr) == expected


@pytest.mark.parametrize("expr", ["10 / 0", "5 * (3 +", "", "abc"])
def test_calculator_rejects_invalid(expr):
    with pytest.raises(ValueError):
        calculator(expr)


@pytest.mark.parametrize("attack", [
    "__import__('os').system('ls')",
    "open('secret.txt').read()",
    "().__class__",
])
def test_calculator_blocks_code_injection(attack):
    with pytest.raises(ValueError):
        calculator(attack)


# --- search ---
def test_search_finds_keyword_case_insensitive():
    assert "30 jours" in search("REMBOURSEMENT possible ?")


def test_search_unknown_returns_not_found():
    assert search("Quelle est la couleur du ciel ?") == "not found"


# --- agent v1 : format de sortie ---
def test_agent_v1_output_format():
    out = AgentV1().run("Calcule 25 * 4")
    assert set(out) == {"answer", "tools", "recovered"}
    assert isinstance(out["tools"], list)


def test_agent_v1_recovers_from_tool_error():
    out = AgentV1().run("Combien font 10 / 0 ?")
    assert out["recovered"] is True
    assert "erreur" in out["answer"]