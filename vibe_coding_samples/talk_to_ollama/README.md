# Talk to Ollama

A real-time voice chat application that allows you to have conversations with Ollama LLM models using speech-to-text and text-to-speech capabilities.

## Prerequisites

- Python 3.11 or higher
- Ollama installed and running locally (default: http://localhost:11434)
- FFmpeg installed (required for audio processing)

### Installing FFmpeg on Windows 11

FFmpeg is required for audio processing in this application. It's used to:

- Convert audio formats between MP3 (from gTTS) and raw audio data
- Resample audio to match the required sample rate (16000 Hz)
- Handle audio streaming and format conversion

Installation steps:

0. Shortest way: `winget install "FFmpeg (Essentials Build)"`

If this fails:

1. Download FFmpeg from the official website: https://ffmpeg.org/download.html
2. Choose the Windows build from https://www.gyan.dev/ffmpeg/builds/
3. Download the "ffmpeg-git-full.7z" file
4. Extract the contents to a folder (e.g., `C:\ffmpeg`)
5. Add the bin directory to your system PATH:
   - Open System Properties (Win + R, type `sysdm.cpl`)
   - Go to Advanced tab → Environment Variables
   - Under System Variables, find and select "Path"
   - Click Edit → New
   - Add the path to the bin directory (e.g., `C:\ffmpeg\bin`)
   - Click OK on all dialogs
6. Verify installation by opening a new terminal and running:
   ```bash
   ffmpeg -version
   ```

## Installation

1. Clone this repository
2. Create a virtual environment using uv:

```bash
uv venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.1:latest

# Server configuration
UVICORN_PORT=7860
DEVELOPMENT_MODE=true  # Set to true for development (enables auto-reload)

# System configuration
SYSTEM_PROMPT=You are a helpful assistant. Please provide concise and clear answers.

# Audio configuration
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
```

### Environment Variables Explained

- **OLLAMA_BASE_URL**: The URL where Ollama is running (default: http://localhost:11434)
- **DEFAULT_MODEL**: The default Ollama model to use (default: llama3.1:latest)
- **UVICORN_PORT**: The port on which the FastAPI server will run (default: 7860)
- **DEVELOPMENT_MODE**: Set to 'true' to enable development features like auto-reload (default: false)
- **SYSTEM_PROMPT**: The system prompt used to configure the LLM's behavior
- **AUDIO_SAMPLE_RATE**: The sample rate for audio processing (default: 16000 Hz)
- **AUDIO_CHANNELS**: The number of audio channels (default: 1 for mono)

## Speech-to-Text (STT)

This application uses FastRTC's built-in Whisper implementation for speech recognition. The STT process works as follows:

1. Audio is captured in real-time through the browser's WebRTC API
2. Audio chunks are sent to the server
3. Whisper processes the audio and converts it to text
4. The text is sent to Ollama for processing
5. The response is converted to speech using the selected TTS engine

## Usage

1. Start Ollama locally:

**Out of scope - Use Docker or Ollama**

2. Run the application:

```bash
python talk_to_ollama.py
```

3. Open your browser and navigate to `http://localhost:7860`

4. Allow microphone access when prompted

5. Start speaking - the application will:
   - Convert your speech to text
   - Send it to Ollama
   - Convert the response to speech
   - Play it back through your speakers

## Features

- Real-time speech recognition
- Automatic model detection and selection
- Conversation history preservation
- Configurable through environment variables
- Open source text-to-speech

## Troubleshooting

- Ensure Ollama is running and accessible at the configured URL
- Check that your microphone is properly connected and enabled
- Verify that all required dependencies are installed
- If audio issues occur, check your browser's audio permissions
- If you encounter audio format conversion errors, verify that FFmpeg is properly installed and accessible
