# rescura/main.py
import sys
from pathlib import Path
from dotenv import load_dotenv
from retrieval.retriever import RescuraRetriever
from agents import TriageAgent, TreatmentAgent, PreventionAgent, FollowUpAgent, ResourceAgent
from input_processing import AudioTranscriber, ImageAnalyzer

# Load environment variables first
load_dotenv()

from utils import (
    setup_logging,
    validate_environment,
    Settings,
    format_scratchpad
)

setup_logging()
validate_environment()
config = Settings()


def main():
    # Initialize components
    retriever = RescuraRetriever()
    transcriber = AudioTranscriber()
    analyzer = ImageAnalyzer()
    
    # Create agent instances
    triage_agent = TriageAgent(retriever)
    treatment_agent = TreatmentAgent(retriever)
    prevention_agent = PreventionAgent(retriever)
    followup_agent = FollowUpAgent(retriever)
    resource_agent = ResourceAgent(retriever)

    print("\n" + "="*40)
    print("🚑 Welcome to Rescura Emergency Assistant")
    print("="*40)

    while True:
        print("\nOptions:")
        print("1. Describe emergency via text")
        print("2. Upload emergency image")
        print("3. Exit")
        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "3":
            print("\nThank you for using Rescura. Stay safe!")
            sys.exit(0)

        user_input = ""
        environment = "urban"  # Default, could be made configurable

        try:
            if choice == "1":
                user_input = input("\nDescribe the emergency situation: ").strip()
                if not user_input:
                    raise ValueError("Please provide a description")
                
            elif choice == "2":
                image_path = input("\nEnter path to image file: ").strip()
                if not Path(image_path).exists():
                    raise FileNotFoundError("Image file not found")
                
                # Analyze image and combine with text input
                image_desc = analyzer.describe(image_path)
                print(f"\n🖼️ Image analysis: {image_desc}")
                user_input = image_desc + "\n" + input("Additional context about the image: ").strip()
            
            else:
                print("\n⚠️ Invalid choice. Please try again.")
                continue

            # Triage assessment
            print("\n🔍 Assessing emergency severity...")
            assessment = triage_agent.assess_emergency(
                symptoms=user_input,
                environment=environment
            )

            print("\n" + "="*40)
            print(f"🚨 Triage Results (Severity {assessment['severity']}/5)")
            print("="*40)
            print(f"Rationale: {assessment['rationale']}")
            print(f"Immediate actions: {', '.join(assessment['immediate_actions'])}")

            # Treatment plan for moderate+ severity
            if assessment['severity'] >= 3:
                print("\n🩺 Generating treatment plan...")
                treatment = treatment_agent.generate_treatment_plan(
                    assessment["diagnosis"],
                    assessment
                )
                print("\n💊 Recommended Treatment:")
                print(treatment)

            # Prevention tips regardless of severity
            print("\n🔒 Generating prevention advice...")
            prevention = prevention_agent.suggest_prevention_measures(
                incident=assessment["diagnosis"],
                environment=environment
            )
            print("\n🛡️ Prevention Measures:")
            print(prevention)

            # Follow-up care
            print("\n📋 Generating follow-up instructions...")
            followup = followup_agent.create_plan(
                treatment=treatment if assessment['severity'] >=3 else "Basic first aid applied",
                severity=assessment['severity']
            )
            print("\n📅 Follow-up Plan:")
            print(f"Monitoring schedule: {followup['monitoring_schedule']}")
            print(f"Red flags: {', '.join(followup['red_flags'])}")

            # Resource finding
            print("\n📍 Locating nearby resources...")
            resources = resource_agent.find_resources(
                resource_type="hospital",
                location=environment
            )
            print("\n🏥 Nearby Medical Facilities:")
            for hospital in resources.get('hospitals', [])[:3]:
                print(f"- {hospital['name']} ({hospital['distance']})")

        except Exception as e:
            print(f"\n⚠️ Error: {str(e)}")
            continue

        input("\nPress Enter to handle another case or Ctrl+C to exit...")

if __name__ == "__main__":
    main()
