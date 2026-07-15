import speech_recognition as sr
import pyttsx3
import nltk

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()


# Define a function to handle voice input
def handle_voice_input():
    """Listen for one phrase and respond. Returns False when the user says goodbye."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Recognize spoken words
        text = r.recognize_google(audio)
        print("You said:", text)

        # Generate a response
        if "hello" in text.lower():
            engine.say("Hello! How can I assist you today?")
        elif "goodbye" in text.lower():
            engine.say("Goodbye! It was nice chatting with you.")
            engine.runAndWait()
            return False
        else:
            engine.say("I'm not sure I understand. Can you please repeat that?")

        # Speak the response
        engine.runAndWait()
    except sr.UnknownValueError:
        print("Sorry, I didn't quite catch that.")
    except sr.RequestError as e:
        print("Speech service is unavailable:", e)

    return True


# Run the voice assistant
if __name__ == "__main__":
    try:
        while handle_voice_input():
            pass
    except KeyboardInterrupt:
        print("\nExiting.")
