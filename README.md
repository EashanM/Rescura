# Rescura

**Rescura** is an AI-powered emergency assistant designed to help users in urgent situations by providing triage, treatment guidance, resource location, and more. It supports both text and voice input, integrates with location and mapping services, and can surface relevant weather/disaster alerts and nearby emergency resources.

---

## Features

- **Triage Agent:** Assesses the severity and likely diagnosis based on user input.
- **Treatment Agent:** Provides step-by-step first aid and treatment plans tailored to the diagnosis and severity.
- **Resource Agent:** Finds nearby hospitals, clinics, and other emergency services.
- **Speech-to-Text:** Accepts voice files and transcribes them for triage and treatment.
- **Weather/Disaster Alerts:** Surfaces current severe weather and disaster alerts for the user's location.
- **Interactive Maps:** Generates maps highlighting hospitals, schools, clinics, police stations, and other locations likely to have first aid resources.
- **Location Awareness:** Uses IP-based geolocation (with user permission) to personalize results.
- **Extensible:** Modular utilities for easy integration into a future frontend or API.

---

## Directory Structure

```
Rescura/
├── agents/                  # TriageAgent, TreatmentAgent, ResourceAgent, etc.
├── retrieval/               # Retriever logic (e.g., FAISS, BM25)
├── utils/
│   ├── speech_to_text.py    # Voice file transcription
│   ├── validation.py        # Input and response validation
│   ├── location.py          # User location via IP geolocation
│   ├── emergency_number.py  # Emergency numbers by country
│   ├── weather_alerts.py    # Weather/disaster alerts (OpenWeatherMap or Weatherbit)
│   ├── map_resources.py     # Google Places API + Folium map generation
├── logs/
│   └── rescura.log          # Application logs
├── main_speech.py           # Main CLI for text/voice triage and treatment
├── main_working.py          # Main CLI with advanced features (location, info add, etc.)
├── main_map.py              # Standalone script to generate resource maps
├── create_local_resources_map.py # Example map generation script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (API keys, etc.)
└── README.md                # This file
```

---

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Rescura
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your `.env` file:**
   ```
   GROQ_API_KEY=your_groq_api_key
   OPENWEATHER_API_KEY=your_openweathermap_api_key
   WEATHERBIT_API_KEY=your_weatherbit_api_key
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   ```

4. **Run the main assistant:**
   ```bash
   python main_speech.py
   ```
   or
   ```bash
   python main_working.py
   ```

---

## Usage

- **Text or Voice Input:** Choose to type or upload a voice file describing the emergency.
- **Triage & Treatment:** The system will assess severity, suggest a diagnosis, and provide treatment steps.
- **Resource Location:** If permitted, the system will use your location to find nearby emergency services and display them on a map.
- **Weather Alerts:** Severe weather or disaster alerts are surfaced for your area.
- **Add More Info:** You can iteratively add more details to refine the assessment.

---

## Customization & Extending

- **Frontend Integration:** All utilities are modular and can be called from a web or mobile frontend.
- **Map Generation:** Use `main_map.py` or `create_local_resources_map.py` to generate resource maps for any location.
- **Alert Utilities:** `utils/weather_alerts.py` and `utils/weather_alerts2.py` can be used to fetch current alerts for any coordinates.

---

## API Keys

- **GROQ_API_KEY:** For LLM-powered triage and treatment.
- **OPENWEATHER_API_KEY / WEATHERBIT_API_KEY:** For weather/disaster alerts.
- **GOOGLE_MAPS_API_KEY:** For places search and geocoding.

---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenWeatherMap](https://openweathermap.org/)
- [Weatherbit.io](https://www.weatherbit.io/)
- [Google Maps Platform](https://cloud.google.com/maps-platform/)
- [Folium](https://python-visualization.github.io/folium/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Pydub](https://github.com/jiaaro/pydub)

---

**Stay safe with Rescura!**
