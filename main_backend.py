import os
from dotenv import load_dotenv
from retrieval.retriever import RescuraRetriever
from agents import TriageAgent, TreatmentAgent, ResourceAgent
from utils.validation import sanitize_input
from utils.location import get_user_location, reverse_geocode
from utils.emergency_number import get_emergency_number
import json
import logging

logging.getLogger("langchain").setLevel(logging.WARNING)
logging.getLogger("langchain.agents").setLevel(logging.WARNING)
logging.getLogger("langchain.tools").setLevel(logging.WARNING)

load_dotenv()

CRITICAL_SEVERITY = 4
CRITICAL_DIAGNOSES = {"myocardial infarction", "stroke", "severe burn", "anaphylaxis", "cardiac arrest"}

def needs_emergency_services(assessment):
    severity = assessment.get("severity", 0)
    diagnosis = assessment.get("diagnosis", "").lower()
    return severity >= CRITICAL_SEVERITY or diagnosis in CRITICAL_DIAGNOSES

class RescuraChatSession:
    def __init__(self, location=None):
        self.retriever = RescuraRetriever()
        self.triage_agent = TriageAgent(self.retriever, os.getenv("GROQ_API_KEY"))
        self.treatment_agent = TreatmentAgent(os.getenv("GROQ_API_KEY"))
        self.resource_agent = ResourceAgent()
        self.location = location
        self.conversation = ""
        self.assessment = None
        self.finished = False
        self.followup_count = 0

    def set_location(self, location):
        self.location = location

    def process_message(self, user_message):
        self.conversation += " " + sanitize_input(user_message)
        while True:
            try:
                assessment = self.triage_agent.assess(self.conversation)
            except Exception as e:
                return {"type": "error", "message": str(e)}
            if "follow_up" in assessment:
                self.followup_count += 1
                if self.followup_count < 4:
                    return {"type": "follow_up", "message": assessment["follow_up"]}
                else:
                    self.conversation += (
                        " You have now asked 4 follow-up questions. "
                        "You must now provide your best clinical judgment and a final answer in the required JSON format. "
                        "Do NOT ask any more questions."
                    )
                    assessment = self.triage_agent.assess(self.conversation)
                    break
            else:
                break

        if "message" in assessment:
            try:
                parsed = json.loads(assessment["message"])
                assessment.update(parsed)
            except Exception:
                pass

        # Treatment plan
        diagnosis = assessment.get('diagnosis', 'unknown')
        severity = assessment.get('severity', '?')
        rationale = assessment.get('rationale', 'N/A')
        actions = assessment.get('immediate_actions', [])
        plan = self.treatment_agent.generate_plan(diagnosis, severity)
        plan_text = plan.content.strip() if hasattr(plan, "content") else str(plan).strip()

        # Emergency services info
        emergency_info = None
        hospitals = None
        if needs_emergency_services(assessment):
            if self.location and self.location.get("city"):
                hospitals = self.resource_agent.find_hospitals(f"{self.location['city']}, {self.location['region']}")
                emergency_info = "This situation may require immediate medical attention. Nearby hospitals have been listed."
            else:
                emergency_info = "This situation may require immediate medical attention, but no location was provided."
        else:
            emergency_info = "No emergency services recommended based on the current assessment."

        # Emergency number
        emergency_number = None
        if self.location and self.location.get("country"):
            emergency_number = get_emergency_number(self.location["country"])

        self.finished = True
        return {
            "type": "assessment",
            "diagnosis": diagnosis,
            "severity": severity,
            "rationale": rationale,
            "immediate_actions": actions,
            "treatment_plan": plan_text,
            "emergency_info": emergency_info,
            "hospitals": hospitals,
            "emergency_number": emergency_number
        }
    
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from React

# For demo: one session per server run
session = RescuraChatSession()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    location = data.get('location')
    # If location is just lat/lng, enrich it
    if location and "lat" in location and "lng" in location and ("city" not in location or "country" not in location):
        location = reverse_geocode(location["lat"], location["lng"])
    if location:
        session.set_location(location)
    response = session.process_message(message)
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)

""" # Example Flask API for frontend integration
if __name__ == "__main__":
    # This is just for demonstration/testing
    print("=== Rescura Chatbot Session ===")
    ask_location = input("May Rescura access your location to find nearby emergency services? (yes/no): ").strip().lower()
    location = None
    if ask_location == "yes":
        location = get_user_location()
        if location and location.get("country"):
            emergency_number = get_emergency_number(location["country"])
            print(f"\n📞 Local Emergency Services Number: {emergency_number}")
        if "error" in location or not location.get("city"):
            print("Could not determine your location. Emergency services will not be shown.")
            location = None
        else:
            print(f"Detected location: {location.get('city', '')}, {location.get('region', '')}, {location.get('country', '')}")
    else:
        print("Location access denied. Emergency services will not be shown.")

    session = RescuraChatSession(location=location)
    while not session.finished:
        user_message = input("\nYou: ")
        response = session.process_message(user_message)
        if response["type"] == "follow_up":
            print("Rescura: " + response["message"])
        elif response["type"] == "assessment":
            print("\n===== Emergency Assessment =====")
            print(f"Possible Condition: {response['diagnosis'].capitalize()}")
            print(f"Severity Level: {response['severity']}/5")
            print(f"Reasoning: {response['rationale']}")
            if response["immediate_actions"]:
                print(f"Immediate Actions: {', '.join(response['immediate_actions'])}")
            print("\nRecommended Treatment Steps:\n" + response["treatment_plan"])
            print("\n" + response["emergency_info"])
            if response["hospitals"]:
                print("\n🏥 Nearby Medical Facilities:")
                print(response["hospitals"])
            if response["emergency_number"]:
                print(f"\n📞 Local Emergency Services Number: {response['emergency_number']}")
        elif response["type"] == "error":
            print("Error:", response["message"])
            print("Raw output:", response.get("raw", ""))
            break
        elif response["type"] == "message":
            print("Rescura:", response["message"])
            break """