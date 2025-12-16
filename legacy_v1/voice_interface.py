import speech_recognition as sr
import pyttsx3
import threading
import queue

class VoiceInterface:
    def __init__(self, on_command_recognized=None):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.on_command = on_command_recognized
        
        # Configure voice
        voices = self.engine.getProperty('voices')
        # Try to find a good english voice, or default
        for voice in voices:
            if "david" in voice.name.lower() or "mark" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
                
        self.engine.setProperty('rate', 170)  # Speed
        self.is_listening = False
        self.cmd_queue = queue.Queue()
        
    def speak(self, text):
        """Speak text in a separate thread"""
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except: pass
        threading.Thread(target=_speak, daemon=True).start()

    def start_listening(self):
        """Start listening loop"""
        if self.is_listening: return
        self.is_listening = True
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop_listening(self):
        self.is_listening = False

    def _listen_loop(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    try:
                        text = self.recognizer.recognize_google(audio)
                        if text and self.on_command:
                            self.on_command(text)
                    except sr.UnknownValueError:
                        pass # No speech recognized
                    except sr.RequestError:
                        self.speak("Voice service unavailable")
                except:
                    continue
