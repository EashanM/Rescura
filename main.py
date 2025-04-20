from retrieval.retriever import RescuraRetriever
from agents import (
    TriageAgent,
    TreatmentAgent,
    PreventionAgent,
    FollowUpAgent,
    ResourceAgent
)
from input_processing import AudioTranscriber, ImageAnalyzer

def main():
    # Initialize components
    retriever = RescuraRetriever()
    transcriber = AudioTranscriber()
    analyzer = ImageAnalyzer()
    
    # Create agent instances
    triage = TriageAgent(retriever)
    treatment = TreatmentAgent(retriever)
    prevention = PreventionAgent(retriever)
    followup = FollowUpAgent(retriever)
    resource = ResourceAgent(retriever)
    
    # Example workflow
    audio_text = transcriber.transcribe("emergency_recording.wav")
    image_desc = analyzer.describe("injury_photo.jpg")
    
    assessment = triage.assess_severity(
        symptoms=audio_text,
        environment="wilderness",
        context=image_desc
    )
    
    if assessment["severity"] > 2:
        treatment_plan = treatment.generate_treatment_plan(
            assessment["diagnosis"],
            assessment
        )
        print(treatment_plan)

if __name__ == "__main__":
    main()
