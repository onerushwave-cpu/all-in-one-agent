# all-in-one-agent

the assistant you been looking for

A Jarvis-style voice assistant: it listens through your microphone, sends what
you say to Claude, and speaks the answer back. Claude can check the current
time and read your Google Calendar on its own when the conversation calls
for it — no hardcoded commands, just talk to it.

## Setup

### 1. System dependencies (Linux)

pyttsx3 needs the eSpeak NG speech engine and PyAudio needs PortAudio:

```bash
sudo apt-get install espeak-ng libespeak-ng1 portaudio19-dev
```

On macOS and Windows no extra system packages are needed (macOS: PortAudio via
`brew install portaudio` if the PyAudio install fails).

### 2. Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Anthropic API key (the brain)

Jarvis thinks with Claude. Get an API key from the
[Claude Console](https://platform.claude.com/) and set it:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 4. NLTK data (one time)

```bash
python setup_nltk.py
```

## Run

```bash
python main.py
```

Say **"Jarvis"** followed by anything — "Jarvis, what's on my calendar
tomorrow?", "Jarvis, what time is it?", or just chat. Say **"goodbye"** to
quit.

Options:

- `python main.py --text` — type instead of talking (no mic or speakers
  needed; great for testing).
- `python main.py --no-wake-word` — respond to everything you say instead of
  waiting for "Jarvis".

Speech recognition uses the Google Web Speech API, so an internet connection
is required while the assistant is listening.

## Google Calendar integration

Jarvis reads your calendar (read-only) whenever you ask about your schedule.
One-time setup:

1. In [Google Cloud Console](https://console.cloud.google.com/), create a
   project, enable the **Google Calendar API**, and create an **OAuth client
   ID** of type *Desktop app*.
2. Download the client secret file and save it as `credentials.json` in this
   directory (it is gitignored — never commit it).
3. Run `python google_calendar.py`. A browser window opens for you to grant
   access; the token is cached in `token.pickle` (also gitignored) so you only
   log in once.

If you skip this, everything else still works — Jarvis will just tell you the
calendar isn't set up when you ask about your schedule. If you change
`SCOPES`, delete `token.pickle` and authenticate again.

## How it works

- `main.py` — the ears and mouth: microphone input (SpeechRecognition), wake
  word detection, and text-to-speech output (pyttsx3).
- `brain.py` — the brain: sends your words to Claude with the conversation
  history (so it remembers context), and exposes tools Claude calls on its
  own: `get_current_datetime` and `get_calendar_events`.
- `google_calendar.py` — Google Calendar OAuth flow and event fetching.
