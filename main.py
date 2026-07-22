"""Jarvis voice assistant: microphone in, Claude in the middle, speech out."""

import argparse
import sys

import anthropic

from brain import JarvisBrain

WAKE_WORD = "jarvis"
EXIT_PHRASES = ("goodbye", "good bye", "exit", "quit", "shut down")


def make_speaker():
    """Return a speak(text) function backed by text-to-speech."""
    import pyttsx3

    engine = pyttsx3.init()

    def speak(text):
        print("Jarvis:", text)
        engine.say(text)
        engine.runAndWait()

    return speak


def make_listener():
    """Return a listen() function that captures one phrase from the mic."""
    import speech_recognition as sr

    recognizer = sr.Recognizer()

    def listen():
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print("Speech service is unavailable:", e)
            return None

    return listen


def strip_wake_word(text):
    """Return the utterance without the wake word, or None if it's absent."""
    lowered = text.lower()
    index = lowered.find(WAKE_WORD)
    if index == -1:
        return None
    remainder = text[index + len(WAKE_WORD):].strip(" ,.!?")
    # Bare "Jarvis" with nothing after it still deserves a response.
    return remainder or "Hello"


def is_exit(text):
    lowered = text.lower()
    return any(phrase in lowered for phrase in EXIT_PHRASES)


def run(get_input, respond, use_wake_word):
    brain = JarvisBrain()
    while True:
        text = get_input()
        if text is None:
            continue
        if not text.strip():
            continue

        if use_wake_word:
            text = strip_wake_word(text)
            if text is None:
                continue  # not talking to Jarvis

        if is_exit(text):
            respond("Goodbye!")
            return

        try:
            reply = brain.ask(text)
        except TypeError:
            # The Anthropic client found no credentials at all.
            print(
                "No Anthropic API key found. Jarvis needs one to think.\n"
                "Get a key at https://platform.claude.com/ and set it:\n"
                "  export ANTHROPIC_API_KEY=sk-ant-...",
                file=sys.stderr,
            )
            return
        except anthropic.AuthenticationError:
            print(
                "Your Anthropic API key was rejected. Set a valid key:\n"
                "  export ANTHROPIC_API_KEY=sk-ant-...",
                file=sys.stderr,
            )
            return
        except anthropic.APIConnectionError:
            respond("I couldn't reach the network. Check your connection.")
            continue
        except anthropic.APIStatusError as e:
            print("Claude API error:", e.status_code, e.message, file=sys.stderr)
            respond("Sorry, I ran into a problem answering that.")
            continue

        respond(reply)


def main():
    parser = argparse.ArgumentParser(description="Jarvis voice assistant")
    parser.add_argument(
        "--text",
        action="store_true",
        help="type instead of talking (no microphone or speakers needed)",
    )
    parser.add_argument(
        "--no-wake-word",
        action="store_true",
        help="respond to everything instead of waiting for 'Jarvis'",
    )
    args = parser.parse_args()

    if args.text:
        def get_input():
            try:
                return input("You: ")
            except (EOFError, KeyboardInterrupt):
                print()
                sys.exit(0)

        def respond(text):
            print("Jarvis:", text)

        use_wake_word = False  # pointless when typing directly at Jarvis
        print("Jarvis text mode. Type 'goodbye' to quit.")
    else:
        get_input = make_listener()
        respond = make_speaker()
        use_wake_word = not args.no_wake_word
        if use_wake_word:
            print("Say 'Jarvis' followed by your request. Say 'goodbye' to quit.")
        else:
            print("Wake word off — I'm listening to everything. Say 'goodbye' to quit.")

    try:
        run(get_input, respond, use_wake_word)
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()
