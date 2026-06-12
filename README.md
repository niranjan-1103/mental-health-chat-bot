# MindGuard: Voice-Enabled Mental Health Chatbot

**MindGuard** is a voice-enabled, safety-first Mental Health Chatbot that integrates empathetic AI conversation with proactive crisis detection and automated emergency protocol redirection. 

Designed with modern AI safety principles in mind, it serves as a companion for wellbeing support, demonstrating how generative AI can be securely bounded to prioritize user safety above all else.

---

## 🌟 Key Features

- **🎙️ Voice-to-Voice Interaction**: Seamless speech-to-text input and text-to-speech feedback using the browser microphone, `SpeechRecognition`, and Google Text-to-Speech (`gTTS`).
- **🛡️ Watchdog Safety Protocol**: A dual-layer crisis detection system. Incoming messages are checked via a hardcoded fast-pass keywords hook on the backend and safety constraints in the Gemini API.
- **🚨 Crisis Override System**: When a safety threshold is crossed, the standard chat is immediately suspended and overridden with a clear emergency screen directing the user to professional hotlines (e.g., 988, 911).
- **📊 Wellbeing Tracking**: A personal dashboard containing a daily mood logger, customizable self-care goals, and motivational quotes.
- **🎨 Glassmorphism UI**: Beautiful, modern dark-mode user interface styled with Tailwind CSS, utilizing micro-animations and smooth transitions.

---

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (Glassmorphism layout), RecordRTC.js
- **Speech Synthesis & Recognition**: `SpeechRecognition` (Google Web Speech API), `gTTS`
- **AI Core**: Google Gemini API (`google-generativeai`)
- **Data Persistence**: Local JSON store (`data.json`)
- **Testing**: PyTest

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher installed.
- A modern web browser (Google Chrome, Microsoft Edge, or Firefox).

### 1. Clone & Navigate to Project
```bash
git clone <your-github-repo-url>
cd "mental health chat bot"
```

### 2. Environment Setup (Virtual Environment)
It is recommended to run the project in a Python virtual environment:

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key
Create a `.env` file in the root of the project directory and insert your Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*Note: If no API key is specified, the application will fallback to a local mock responder so you can still test the interface and safety protocols without an API key.*

### 5. Run the Application
You can start the backend web server in two ways:

- **Option A (Windows Double-Click)**: Double-click the `start.bat` file in the root directory.
- **Option B (Command Line)**: Run the following command in your terminal:
  ```bash
  uvicorn main:app --reload
  ```

Once started, open your browser and go to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📁 Repository Structure

- `main.py`: Central FastAPI routing, mounting frontend, and database helper methods.
- `chat_logic.py`: Connects to Gemini, sets the empathetic system prompt, and parses metadata tags (e.g., mood, override flags).
- `voice_engine.py`: Handles Speech-to-Text conversion and Text-to-Speech audio compilation.
- `data.json`: Local JSON database representing stored moods and active goals.
- `start.bat`: Simple batch script to automate virtual environment activation and start the server on Windows.
- `static/`: Contains HTML structure, styling, audio outputs, and browser JavaScript scripts.
- `tests/`: Automated unit and integration testing suite.

---

## 📘 In-Depth Documentation

For more specific information on the system's design and logic flow, check out:
- 📖 [Project Guide](file:///c:/Users/Niranjan%20N%20R/OneDrive/Desktop/mental%20health%20chat%20bot/Project_Guide.md) - Overview of architecture and how to run locally.
- ⚙️ [Technical Design](file:///c:/Users/Niranjan%20N%20R/OneDrive/Desktop/mental%20health%20chat%20bot/Technical_Design.md) - System modules, layers, and security considerations.
- 🔄 [Application Flow Design](file:///c:/Users/Niranjan%20N%20R/OneDrive/Desktop/mental%20health%20chat%20bot/Flow_Design.md) - Step-by-step description of voice loops and crisis triggers.

---

## 🔒 License
This project is open-source under the [MIT License](LICENSE).
