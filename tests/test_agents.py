import os
import pytest
from dotenv import load_dotenv
from agents.triage_agent import TriageAgent
from agents.treatment_agent import TreatmentAgent
from agents.resource_agent import ResourceAgent
from retrieval.retriever import RescuraRetriever

load_dotenv()

@pytest.fixture(scope="module")
def retriever():
    # Use the real RescuraRetriever for retrieval tasks
    return RescuraRetriever()

@pytest.fixture(scope="module")
def triage_agent(retriever):
    return TriageAgent(retriever, os.getenv("GROQ_API_KEY"))

@pytest.fixture(scope="module")
def treatment_agent(retriever):
    return TreatmentAgent(retriever, os.getenv("GROQ_API_KEY"))

@pytest.fixture(scope="module")
def resource_agent():
    return ResourceAgent()

def test_triage_agent(triage_agent):
    assessment = triage_agent.assess("Chest pain, sweating, left arm numbness")
    assert isinstance(assessment, dict)
    assert "severity" in assessment or "error" in assessment

def test_treatment_agent(treatment_agent):
    plan = treatment_agent.plan("fracture", 3)
    assert isinstance(plan, str) or isinstance(plan, dict)

def test_resource_agent(resource_agent):
    hospitals = resource_agent.find_hospitals("Mountain View, CA")
    assert isinstance(hospitals, str)