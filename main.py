import speech_recognition as sr
import pyttsx3
import nltk

from google_calendar import authenticate, get_events

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
        elif "what's my schedule" in text.lower():
            try:
                service = authenticate()
                events = get_events(service)
            except Exception as e:
                print("Calendar error:", e)
                engine.say("Sorry, I couldn't reach your calendar.")
            else:
                # Respond with the events
                if events:
                    engine.say("You have the following events:")
                    for event in events:
                        engine.say(event.get('summary', 'an untitled event'))
                else:
                    engine.say("You have no upcoming events.")
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
