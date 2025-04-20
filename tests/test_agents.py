import pytest
from unittest.mock import MagicMock
from agents.triage_agent import TriageAgent
from agents.treatment_agent import TreatmentAgent
from agents.prevention_agent import PreventionAgent
from agents.followup_agent import FollowUpAgent
from agents.resource_agent import ResourceAgent

class DummyRetriever:
    def get_relevant_documents(self, query, k=3):
        class Doc:
            page_content = "Sample first aid content"
        return [Doc()]

@pytest.fixture
def retriever():
    return DummyRetriever()

def test_triage_agent_basic(retriever):
    agent = TriageAgent(retriever)
    result = agent.assess_emergency("Severe bleeding from leg", "wilderness")
    assert isinstance(result, dict)
    assert "severity" in result

def test_treatment_agent_basic(retriever):
    agent = TreatmentAgent(retriever)
    plan = agent.generate_treatment_plan("fracture", {"severity": 4})
    assert isinstance(plan, str) or isinstance(plan, dict)

def test_prevention_agent_basic(retriever):
    agent = PreventionAgent(retriever)
    advice = agent.suggest_prevention("burn", "urban")
    assert isinstance(advice, str) or isinstance(advice, dict)

def test_followup_agent_basic(retriever):
    agent = FollowUpAgent(retriever)
    plan = agent.create_plan("immobilization", 3)
    assert isinstance(plan, dict)

def test_resource_agent_basic(retriever):
    agent = ResourceAgent(retriever)
    resources = agent.find_resources("hospital", "urban")
    assert isinstance(resources, dict)
