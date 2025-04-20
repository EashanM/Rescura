import os
from unittest.mock import MagicMock
from agents.triage_agent import TriageAgent
from agents.treatment_agent import TreatmentAgent
from agents.resource_agent import ResourceAgent
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize with your Groq API key
triage = TriageAgent(retriever, GROQ_API_KEY)
treatment = TreatmentAgent(retriever, GROQ_API_KEY)
resource = ResourceAgent(GROQ_API_KEY)

# Triage assessment
assessment = triage.assess("Chest pain, sweating, left arm numbness")
if assessment['severity'] >= 3:
    # Get treatment plan
    plan = treatment.plan("heart attack", assessment['severity'])
    # Find resources
    hospitals = resource.find("hospital", "current location")