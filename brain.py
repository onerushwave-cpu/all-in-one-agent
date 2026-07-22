"""The AI brain of Jarvis: Claude with tools it can call on its own."""

from datetime import datetime

import anthropic
from anthropic import beta_tool

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = """\
You are Jarvis, a personal voice assistant.

Your responses are spoken aloud through text-to-speech, so:
- Keep answers short and conversational — one to three sentences for most questions.
- Never use markdown, bullet points, code blocks, or emoji.
- Say dates and times naturally ("tomorrow at 3 PM", not "2026-07-17T15:00").

Use your tools when the user asks about their schedule, calendar, or the
current date or time. If a tool fails, tell the user plainly what went wrong.
"""


@beta_tool
def get_current_datetime() -> str:
    """Get the current local date, time, and day of the week."""
    return datetime.now().strftime("%A, %B %d, %Y, %I:%M %p")


@beta_tool
def get_calendar_events(max_results: int = 10) -> str:
    """List the user's upcoming Google Calendar events.

    Args:
        max_results: Maximum number of upcoming events to return.
    """
    try:
        from google_calendar import authenticate, get_events

        service = authenticate()
        events = get_events(service, max_results=max_results)
    except FileNotFoundError:
        return (
            "Error: credentials.json not found. Google Calendar is not set up "
            "yet (see the README)."
        )
    except Exception as e:
        return f"Error: could not reach Google Calendar ({e})"

    if not events:
        return "No upcoming events."

    lines = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        lines.append(f"{start} — {event.get('summary', '(no title)')}")
    return "\n".join(lines)


class JarvisBrain:
    """Holds the conversation with Claude and runs its tool calls."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.messages = []

    def ask(self, text: str) -> str:
        """Send one user utterance to Claude and return the spoken reply."""
        self.messages.append({"role": "user", "content": text})

        runner = self.client.beta.messages.tool_runner(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=[get_current_datetime, get_calendar_events],
            messages=self.messages,
        )

        # Mirror the runner's turns into our history so Jarvis remembers
        # the whole conversation (including tool calls) across questions.
        last = None
        for message in runner:
            last = message
            self.messages.append({"role": "assistant", "content": message.content})
            tool_response = runner.generate_tool_call_response()
            if tool_response is not None:
                self.messages.append(tool_response)

        if last is None:
            return "Sorry, something went wrong and I have no answer."
        reply = "".join(b.text for b in last.content if b.type == "text").strip()
        return reply or "Sorry, I don't have an answer for that."
