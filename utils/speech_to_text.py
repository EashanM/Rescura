import speech_recognition as sr
from pydub import AudioSegment
import os 
import sys 

sys.path.append(os.path.abspath(os.curdir))  #


def transcribe_audio(audio_path: str) -> str:
    """Transcribe an audio file (wav, mp3, m4a) to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    # Convert to wav if needed
    if not audio_path.lower().endswith(".wav"):
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_path, format="wav")
        audio_path = wav_path
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
    
if __name__ == "__main__":
    # Example usage
    audio_file = "data/trial_inputs/Voice/G_St_2.m4a"
    transcription = transcribe_audio(audio_file)
    print("Transcription:", transcription)