# Hostile Job Interview Audio Generator

This script generates an AI-generated audio file that simulates a hostile job interview with a heartbeat sound in the background.

## Features

- AI-generated voice using Google Text-to-Speech
- Hostile interview questions covering:
  1. Joke telling and evaluation
  2. Personal challenges and discussion
  3. Secret sharing and assessment
  4. Final rejection
- Realistic heartbeat sound (lub-dub pattern at 85 BPM) playing throughout
- Pauses for participant responses during the interview

## Requirements

- Python 3.7+
- ffmpeg (required by pydub for audio processing)

## Installation

### 1. Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

## Usage

Simply run the script:

```bash
python generate_interview.py
```

The script will:
1. Generate all interview segments using text-to-speech
2. Create a heartbeat background sound
3. Mix them together
4. Export as `hostile_interview.mp3`

The process takes about 30-60 seconds depending on your internet connection (for the TTS API calls).

## Output

The generated audio file (`hostile_interview.mp3`) will be approximately 3-4 minutes long and includes:
- Introduction asking participants to form pairs/trios
- Three rounds of questions with discussion time
- A hostile rejection at the end
- Continuous heartbeat sound throughout

## Customization

You can modify the script to adjust:
- Interview questions (in the `generate_interview()` function)
- Pause durations for participant responses
- Heartbeat rate (BPM parameter in `generate_heartbeat()`)
- Voice language (lang parameter in `text_to_speech()`)

## Notes

- The script requires an internet connection for Google Text-to-Speech API
- The heartbeat is synthesized using sine waves to create a realistic lub-dub pattern
- Audio quality is set to 192kbps MP3
