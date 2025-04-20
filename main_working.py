import os
from dotenv import load_dotenv
from retrieval.retriever import RescuraRetriever
from agents import TriageAgent, TreatmentAgent, ResourceAgent
from utils.speech_to_text import transcribe_audio
from utils.validation import sanitize_input
from utils.location import get_user_location
from utils.emergency_number import get_emergency_number

load_dotenv()

CRITICAL_SEVERITY = 4
CRITICAL_DIAGNOSES = {"myocardial infarction", "stroke", "severe burn", "anaphylaxis", "cardiac arrest"}

def needs_emergency_services(assessment):
    severity = assessment.get("severity", 0)
    diagnosis = assessment.get("diagnosis", "").lower()
    return severity >= CRITICAL_SEVERITY or diagnosis in CRITICAL_DIAGNOSES

def main():
    retriever = RescuraRetriever()
    triage_agent = TriageAgent(retriever, os.getenv("GROQ_API_KEY"))
    treatment_agent = TreatmentAgent(os.getenv("GROQ_API_KEY"))
    resource_agent = ResourceAgent()

    print("=== Rescura Emergency Assistant ===")

    location = None
    ask_location = input("May Rescura access your location to find nearby emergency services? (yes/no): ").strip().lower()
    if ask_location == "yes":
        location = get_user_location()
        location = "Moscow, Russia"
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

            while True:
                # Triage assessment
                assessment = triage_agent.assess(user_input)
                severity = assessment.get('severity', '?')
                diagnosis = assessment.get('diagnosis', 'unknown')
                rationale = assessment.get('rationale', 'N/A')
                actions = assessment.get('immediate_actions', [])

                # Treatment plan
                plan = treatment_agent.generate_plan(diagnosis, severity)
                plan_text = plan.content.strip() if hasattr(plan, "content") else str(plan).strip()

                # Clean, unified output
                print("\n===== Emergency Assessment =====")
                print(f"Possible Condition: {diagnosis.capitalize()}")
                print(f"Severity Level: {severity}/5")
                print(f"Reasoning: {rationale}")
                if actions:
                    print(f"Immediate Actions: {', '.join(actions)}")
                print("\nRecommended Treatment Steps:\n" + plan_text)

                # Conditional emergency services
                if needs_emergency_services(assessment) and location and location.get("city"):
                    print("\n⚠️ This situation may require immediate medical attention.")
                    print("\n📍 Locating nearby hospitals...")
                    hospitals = resource_agent.find_hospitals(f"{location['city']}, {location['region']}")
                    print("\n🏥 Nearby Medical Facilities:")
                    print(hospitals)
                elif needs_emergency_services(assessment):
                    print("\n⚠️ This situation may require immediate medical attention, but no location was provided.")
                else:
                    print("\nℹ️ No emergency services recommended based on the current assessment.")


                # Ask if user wants to add more info
                more = input("\nWould you like to add more information? (yes/no): ").strip().lower()
                if more == "yes":
                    extra = input("Please provide additional details: ").strip()
                    user_input += " " + sanitize_input(extra)
                else:
                    break

        except Exception as e:
            print(f"\n⚠️ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()