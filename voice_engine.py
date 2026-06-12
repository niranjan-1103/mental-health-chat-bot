import speech_recognition as sr
from gtts import gTTS
import os
import uuid

def speech_to_text(audio_file_path: str) -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            # recognize_google works best with WAV
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
    except Exception as e:
        print(f"Audio processing error: {e}")
        return ""

def text_to_speech(text: str, output_dir: str = "static/audio") -> str:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(output_dir, filename)
        tts.save(filepath)
        return filename
    except Exception as e:
        print(f"TTS error: {e}")
        return ""
