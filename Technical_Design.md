# MindGuard: Technical Design Document

## Overview

MindGuard is an AI-powered voice companion specifically designed to act as an empathetic, supportive mental health assistant. The application integrates advanced Large Language Models (LLMs) with real-time speech-to-text and text-to-speech functionality to provide a natural, conversational experience.

## Technology Stack

The application is structured as a full-stack web application with the following core components:

*   **Frontend (User Interface):**
    *   **HTML/Vanilla JS:** Provides the structure and interaction logic for the client.
    *   **Tailwind CSS (via CDN):** Utilized for rapid, modern styling, responsive design, and seamless Dark Mode implementation.
    *   **RecordRTC.js:** A robust library used to capture audio streams directly from the user's browser, enabling voice interactions.
*   **Backend (Server & APIs):**
    *   **FastAPI (Python):** Chosen for its high performance, automatic documentation, and native asynchronous support. It serves both the static HTML files and the backend API endpoints.
    *   **Uvicorn:** The ASGI web server used to run the FastAPI application.
*   **AI Integration Engine:**
    *   **Google Gemini AI (`google.generativeai`):** Serves as the cognitive engine for understanding user input, determining context, extracting emotional states (mood detection), and formulating empathetic responses.
*   **Voice Processing System:**
    *   **`SpeechRecognition` (Google Web Speech API / local audio parsing):** Converts incoming `.wav` audio blobs into actionable text strings.
    *   **`gTTS` (Google Text-to-Speech):** Synthesizes the AI's textual responses into human-like audio files to be played back on the client side.
*   **Data Persistence Layer:**
    *   **Server-Side JSON (`data.json`):** A lightweight, server-hosted JSON file utilized to persist stateful application data, including user goals and logged moods, preserving them across individual sessions without the overhead of a dedicated SQL/NoSQL database service.

## Application Architecture

The architecture follows a standard Client-Server model with discrete modules.

1.  ### `main.py` (The Routing Layer)
    Acts as the central conductor. It mounts the frontend application, initializes the simple JSON database (`load_db`, `save_db`), and exposes necessary internal RESTful APIs (`/api/chat`, `/api/goals`, `/api/mood`, `/api/dashboard`). It also coordinates the flow of data utilizing helper functions from other modules.

2.  ### `chat_logic.py` (The AI Cognitive Layer)
    Houses the interaction logic with the Gemini model. This module maintains critical `system prompts` that enforce the application's rules:
    *   Enforcing safety bounds and filtering harmful intent.
    *   Extracting hidden metadata, such as dynamic mood tracking via appended tags (`[MOOD:Sad]`).
    *   Generating contextually appropriate, responsive empathetic dialogue.

3.  ### `voice_engine.py` (The Sensory Layer)
    Encapsulates all processing concerned with reading user voice and synthesizing the AI’s voice response.

## Security & Privacy Considerations

*   The implementation inherently processes all critical operations server-side, never exposing the model's API keys directly to the frontend.
*   No personal identifiable information (PII) is durably saved in the audio format. Uploaded audio files could be cleared via scheduled chron jobs in a production environment.
*   A localized fallback "Crisis Override" system exists to immediately short-circuit AI generation if predefined emergency keywords are detected, guaranteeing strict safety protocol obedience.
