# all-in-one-agent
the assistant you been looking for

A voice assistant that listens through your microphone, recognizes what you
say, and talks back.

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

### 3. NLTK data (one time)

```bash
python setup_nltk.py
```

## Run

```bash
python main.py
```

Say **hello** to get a greeting, or **goodbye** to end the conversation.
Speech recognition uses the Google Web Speech API, so an internet connection
is required while the assistant is listening.

## Google Calendar integration

`google_calendar.py` connects to your Google Calendar (read-only). One-time
setup:

1. In [Google Cloud Console](https://console.cloud.google.com/), create a
   project, enable the **Google Calendar API**, and create an **OAuth client
   ID** of type *Desktop app*.
2. Download the client secret file and save it as `credentials.json` in this
   directory (it is gitignored — never commit it).
3. Run `python google_calendar.py`. A browser window opens for you to grant
   access; the token is cached in `token.pickle` (also gitignored) so you only
   log in once.

After that it prints your next 10 upcoming events. If you change `SCOPES`,
delete `token.pickle` and authenticate again.
