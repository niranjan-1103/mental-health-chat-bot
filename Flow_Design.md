# MindGuard: Application Flow Design

This document maps out the essential user journeys and internal data cycles within the MindGuard application.

## 1. Primary Interaction Flow (The Voice Loop)

The most prominent feature is the conversational interface. The progression occurs as follows:

1.  **Audio Capture (Frontend):** 
    *   The user accesses the *Chat* view and triggers the microphone button.
    *   `RecordRTC` begins capturing the audio stream from the browser environment.
    *   Upon stopping, the audio is packaged as a `.wav` blob.
2.  **Data Transmission:**
    *   The `.wav` payload is uploaded to the backend via a `multipart/form-data` POST request to `/api/chat`.
3.  **Sensory Conversion (Backend):**
    *   `main.py` saves the temporary file and calls `voice_engine.speech_to_text()` to convert the audio payload into a text string.
4.  **Cognitive Evaluation & Rules Engine:**
    *   The transcribed text is scanned by a hard-coded Crisis Hook (`check_for_crisis`). 
    *   If a safety breach is detected, the flow immediately aborts typical AI processing and injects a `[CRISIS_OVERRIDE]` response.
    *   Otherwise, the text is handed to `chat_logic.get_chat_response()`. The Gemini AI interprets the input and provides an empathetic response and optional metadata tags (e.g., `[MOOD:Calm]`).
5.  **Output Synthesis:**
    *   Metadata tags are parsed, actioned (e.g., logging the mood to the DB), and scrubbed from the final display string.
    *   The cleaned string is passed to `voice_engine.text_to_speech()`, generating an output `.mp3`.
6.  **Client Reception:**
    *   The backend returns a JSON payload containing the dialogue text, a path to the generated audio file, and any relevant state flags.
    *   The frontend displays the text in the Chat UI and automatically executes the audio file.

## 2. Wellbeing Tracking Flow (Goals & Moods)

MindGuard introduces stateful tracking for ongoing, continuous support.

*   **Initialization:** Upon accessing the *Wellbeing* tab, the frontend issues a GET request to `/api/dashboard` to retrieve currently active goals, historical user moods, and daily resource snippets (tips/quotes).
*   **Logging Moods:** The user clicks an emoji representing their current emotional state. A POST request is sent to `/api/mood`. The backend appends this timestamped state to `data.json`.
*   **Managing Goals:** The user can add a custom goal text input. This fires a POST to `/api/goals`. Toggling a goal's completion status sends a PUT request to `/api/goals/{id}`, flipping its boolean state within the structured JSON data store. 

## 3. The Crisis Override Mechanism

Safety is prioritized above arbitrary generative text. The application utilizes a dual-layer override mechanism:

*   **Layer 1 (The AI Prompt):** The system instructions injected into Gemini contain explicit, uncompromising directives outlining triggers that require the AI to output exactly `[CRISIS_OVERRIDE]`.
*   **Layer 2 (The Hardcoded Fallback):** Before any API request is fired to the AI, a Python array of extreme keywords parses the plain text transcription. If a match is found, the generation is skipped entirely.
*   **Trigger Result:** When the frontend receives a response where the `crisis = True` flag is active, it hides the standard application logic entirely, obscuring the screen with a high-contrast Red modal detailing emergency hotlines and preventing further generation until the application loop is explicitly restarted.
