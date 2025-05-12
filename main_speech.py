import os
from dotenv import load_dotenv
from retrieval.retriever import RescuraRetriever
from agents import TriageAgent, TreatmentAgent, ResourceAgent
from utils.speech_to_text import transcribe_audio
from utils.validation import sanitize_input

load_dotenv()

def main():
    retriever = RescuraRetriever()
    triage_agent = TriageAgent(retriever, os.getenv("GROQ_API_KEY"))
    treatment_agent = TreatmentAgent(os.getenv("GROQ_API_KEY"))
    resource_agent = ResourceAgent()

    print("=== Rescura Emergency Assistant ===")
    while True:
        try:
            mode = input("\nType 'voice' to use an audio file, or 'text' to type your emergency (or 'exit' to quit): ").strip().lower()
            if mode == "exit":
                print("Goodbye!")
                break

            if mode == "voice":
                audio_path = input("Enter the path to your audio file: ").strip()
                user_input = transcribe_audio(audio_path)
                if not user_input:
                    print("Could not transcribe audio. Please try again.")
                    continue
                print(f"Transcribed Text: {user_input}")
            elif mode == "text":
                user_input = input("Describe the emergency situation: ").strip()
            else:
                print("Invalid option.")
                continue

            user_input = sanitize_input(user_input)

            # Triage assessment
            assessment = triage_agent.assess(user_input)
            print(f"\n🚨 Triage Results (Severity {assessment.get('severity', '?')}/5)")
            print(f"Diagnosis: {assessment.get('diagnosis', 'unknown')}")
            print(f"Rationale: {assessment.get('rationale', 'N/A')}")
            if "immediate_actions" in assessment:
                print(f"Immediate actions: {', '.join(assessment['immediate_actions'])}")

            # Treatment plan
            diagnosis = assessment.get("diagnosis", "unknown")
            plan = treatment_agent.generate_plan(diagnosis, assessment.get("severity", 3))
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