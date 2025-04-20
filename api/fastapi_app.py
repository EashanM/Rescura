from fastapi import FastAPI, UploadFile
from input_processing.audio_transcriber import AudioTranscriber
from input_processing.image_analyzer import ImageAnalyzer
from agents.triage_agent import TriageAgent
from retrieval.retriever import RescuraRetriever

app = FastAPI()
retriever = RescuraRetriever()
triage_agent = TriageAgent(retriever)

@app.post("/process-emergency")
async def process_emergency(
    audio: UploadFile,
    image: UploadFile = None
):
    # Process audio
    transcriber = AudioTranscriber()
    text_input = transcriber.transcribe(audio.file)
    
    # Process image
    image_desc = ""
    if image:
        analyzer = ImageAnalyzer()
        image_desc = analyzer.describe(image.file)
    
    # Combine inputs
    full_input = f"{text_input}. Image context: {image_desc}"
    
    # Get triage assessment
    assessment = triage_agent.assess_severity(
        symptoms=full_input,
        environment="urban"
    )
    
    return {
        "assessment": assessment,
        "next_steps": "/treatment etc."
    }
