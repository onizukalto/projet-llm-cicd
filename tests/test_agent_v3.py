import pytest
import agent_v3
from agent_v3 import AgentV3


class FakePipeline:
    """Se comporte comme un pipeline transformers, mais renvoie une réponse fixée à l'avance."""

    def __init__(self, reply):
        self.reply = reply
        self.calls = []

    def __call__(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        return [{"generated_text": messages + [{"role": "assistant", "content": self.reply}]}]


@pytest.fixture
def make_agent(monkeypatch):
    """Crée un AgentV3 dont le modèle répond toujours `reply`."""
    def _make(reply):
        fake = FakePipeline(reply)
        monkeypatch.setattr(agent_v3, "pipeline", lambda *args, **kwargs: fake)
        return AgentV3(), fake
    return _make


def test_calculator_choice_runs_calculation(make_agent):
    agent, _ = make_agent("calculator")
    out = agent.run("Combien font (2 + 3) * 4 ?")
    assert out == {"answer": "20", "tools": ["calculator"], "recovered": False}


def test_search_choice_ignores_numbers_in_question(make_agent):
    agent, _ = make_agent("search")
    out = agent.run("La garantie couvre-t-elle un usage 24/7 ?")
    assert out["tools"] == ["search"]
    assert "2 ans" in out["answer"]


def test_calculator_choice_without_expression_falls_back_to_search(make_agent):
    agent, _ = make_agent("calculator")
    out = agent.run("Quelle est la politique de remboursement ?")
    assert out["tools"] == ["search"]


def test_invalid_expression_is_recovered(make_agent):
    agent, _ = make_agent("calculator")
    out = agent.run("Combien font 10 / 0 ?")
    assert out["recovered"] is True
    assert "erreur" in out["answer"]


@pytest.mark.parametrize("reply", ["Calculator.", "Réponse : calculator", "  CALCULATOR\n"])
def test_noisy_model_output_is_understood(make_agent, reply):
    agent, _ = make_agent(reply)
    assert agent.run("Calcule 25 * 4")["answer"] == "100"


@pytest.mark.parametrize("reply", ["", "je ne sais pas", "🤖"])
def test_garbage_model_output_defaults_to_search(make_agent, reply):
    agent, _ = make_agent(reply)
    assert agent.run("Calcule 25 * 4")["tools"] == ["search"]


def test_model_is_called_deterministically(make_agent):
    agent, fake = make_agent("search")
    agent.run("Quels sont les délais de livraison ?")
    messages, kwargs = fake.calls[0]
    assert kwargs.get("do_sample") is False
    assert "délais de livraison" in messages[-1]["content"]