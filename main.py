import os
from dotenv import load_dotenv
from retrieval.retriever import RescuraRetriever
from agents import TriageAgent, TreatmentAgent, ResourceAgent

load_dotenv()

def main():
    # Initialize retriever and agents
    retriever = RescuraRetriever()
    triage_agent = TriageAgent(retriever, os.getenv("GROQ_API_KEY"))
    treatment_agent = TreatmentAgent(os.getenv("GROQ_API_KEY"))
    resource_agent = ResourceAgent()

    print("=== Rescura Emergency Assistant ===")
    while True:
        try:
            user_input = input("\nDescribe the emergency situation (or type 'exit' to quit): ").strip()
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            # Triage assessment
            print("\n🔍 Assessing emergency severity...")
            assessment = triage_agent.assess(user_input)
            print(f"\n🚨 Triage Results (Severity {assessment.get('severity', '?')}/5)")
            print(f"Diagnosis: {assessment.get('diagnosis', 'unknown')}")
            print(f"Rationale: {assessment.get('rationale', 'N/A')}")
            if "immediate_actions" in assessment:
                print(f"Immediate actions: {', '.join(assessment['immediate_actions'])}")

            # Treatment plan
            print("\n🩺 Generating treatment plan...")
            diagnosis = assessment.get("diagnosis", "unknown")
            plan = treatment_agent.generate_plan("unknown" if "diagnosis" not in assessment else assessment["diagnosis"], assessment.get("severity", 3))
            if hasattr(plan, "content"):
                print("\n💊 Recommended Treatment Guidelines:\n")
                print(plan.content.strip())
            else:
                print("\n💊 Recommended Treatment Guidelines:\n")
                print(str(plan).strip())

            # Resource finding
            print("\n📍 Locating nearby hospitals...")
            hospitals = resource_agent.find_hospitals("Stanford, CA")
            print("\n🏥 Nearby Medical Facilities:")
            print(hospitals)

        except Exception as e:
            print(f"\n⚠️ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()