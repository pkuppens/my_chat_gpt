import io
import logging
import os
import wave
from pathlib import Path
from typing import Dict, List, Optional

import gradio as gr
import numpy as np
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastrtc import ReplyOnPause, Stream
from fastrtc.utils import audio_to_bytes
from gtts import gTTS
from pydantic import BaseModel

# Configure logging with detailed format
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEVELOPMENT_MODE", "false").lower() == "true" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()
logger.info("Environment variables loaded successfully")

# Configuration
logger.info("Initializing application configuration...")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.1:latest")
UVICORN_PORT = int(os.getenv("UVICORN_PORT", "7860"))
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant. Please provide concise and clear answers.")
AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", "1"))
logger.info(
    f"Configuration loaded: OLLAMA_BASE_URL={OLLAMA_BASE_URL}, DEFAULT_MODEL={DEFAULT_MODEL}, UVICORN_PORT={UVICORN_PORT}, DEVELOPMENT_MODE={DEVELOPMENT_MODE}"
)

# System prompt for the LLM
logger.info("System prompt initialized")


class Message(BaseModel):
    role: str
    content: str


class ChatHistory:
    def __init__(self):
        logger.info("Initializing new chat history")
        self.messages: List[Dict] = []
        self.add_system_message()

    def add_system_message(self):
        logger.debug("Adding system message to chat history")
        self.messages.append({"role": "system", "content": SYSTEM_PROMPT})

    def add_message(self, role: str, content: str):
        logger.debug(f"Adding {role} message to chat history: {content[:50]}...")
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict]:
        return self.messages


def get_available_models() -> List[str]:
    """Fetch available models from Ollama API"""
    logger.info("Fetching available models from Ollama...")
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        models = [model["name"] for model in response.json()["models"]]
        logger.info(f"Successfully fetched {len(models)} models: {', '.join(models)}")
        return models
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")


def select_model(models: List[str], preferred_model: Optional[str] = None) -> str:
    """Select model based on configuration or available models"""
    logger.info(f"Selecting model (preferred: {preferred_model}, default: {DEFAULT_MODEL})")

    if preferred_model and preferred_model in models:
        logger.info(f"Using preferred model: {preferred_model}")
        return preferred_model

    if DEFAULT_MODEL in models:
        if preferred_model:
            logger.warning(f"Preferred model '{preferred_model}' not found, falling back to default model '{DEFAULT_MODEL}'")
        logger.info(f"Using default model: {DEFAULT_MODEL}")
        return DEFAULT_MODEL

    if not models:
        logger.error("No models available")
        raise HTTPException(status_code=500, detail="No models available")

    error_msg = f"Neither preferred model '{preferred_model}' nor default model '{DEFAULT_MODEL}' are available. Available models: {', '.join(models)}"
    logger.error(error_msg)
    raise HTTPException(status_code=500, detail=error_msg)


def text_to_speech(text: str) -> tuple[int, np.ndarray]:
    """Convert text to speech using gTTS"""
    logger.info(f"Converting text to speech: {text[:50]}...")
    tts = gTTS(text=text, lang="en")
    tts.save("temp.mp3")
    logger.debug("TTS audio saved to temp.mp3")

    # Convert to numpy array (simplified for example)
    # In a real implementation, you would use proper audio processing
    audio_data = np.zeros((AUDIO_SAMPLE_RATE * 2,), dtype=np.float32)
    logger.debug(f"Generated audio data with shape: {audio_data.shape}")
    return AUDIO_SAMPLE_RATE, audio_data


def process_audio(
    audio: tuple[int, np.ndarray], chat_history: Optional[List[Dict]] = None
) -> tuple[tuple[int, np.ndarray], List[Dict]]:
    """Process audio input and generate response"""
    logger.info("Processing new audio input")

    # Validate input parameters
    if not isinstance(audio, tuple) or len(audio) != 2:
        raise ValueError("Audio input must be a tuple of (sample_rate, audio_data)")

    sample_rate, audio_data = audio
    if not isinstance(sample_rate, int) or not isinstance(audio_data, np.ndarray):
        raise ValueError("Audio input must be (int, np.ndarray)")

    if audio_data.dtype != np.float32:
        logger.warning(f"Converting audio data from {audio_data.dtype} to float32")
        audio_data = audio_data.astype(np.float32)

    logger.debug(f"Audio input: sample_rate={sample_rate}, shape={audio_data.shape}, dtype={audio_data.dtype}")

    chat_history = chat_history or []

    # Convert audio to text using FastRTC's Whisper
    logger.debug("Converting audio to bytes")
    try:
        audio_bytes = audio_to_bytes(audio)
        logger.debug(f"Converted audio to {len(audio_bytes)} bytes")
    except Exception as e:
        logger.error(f"Error converting audio to bytes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

    # Use FastRTC's Whisper for speech recognition
    logger.info("Initializing Whisper for speech recognition")
    from fastrtc.whisper import Whisper

    whisper = Whisper()
    text = whisper.transcribe(audio_bytes)
    logger.info(f"Speech recognition completed: {text[:50]}...")

    # Get response from Ollama
    logger.info("Preparing messages for Ollama")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": text})

    try:
        logger.info("Sending request to Ollama")
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat", json={"model": select_model(get_available_models()), "messages": messages}
        )
        response.raise_for_status()
        response_text = response.json()["message"]["content"]
        logger.info(f"Received response from Ollama: {response_text[:50]}...")

        # Convert response to speech
        logger.info("Converting response to speech")
        audio_response = text_to_speech(response_text)

        # Update chat history
        logger.debug("Updating chat history")
        chat_history.append({"role": "user", "content": text})
        chat_history.append({"role": "assistant", "content": response_text})

        return audio_response, chat_history
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get response from Ollama: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get response from Ollama: {str(e)}")


# Create FastAPI app
logger.info("Initializing FastAPI application...")
app = FastAPI()
logger.info("FastAPI application initialized successfully")

# Create Gradio interface
logger.info("Setting up Gradio interface...")
chatbot = gr.Chatbot(type="messages")
stream = Stream(
    modality="audio",
    mode="send-receive",
    handler=ReplyOnPause(process_audio),
    additional_outputs_handler=lambda a, b: b,
    additional_inputs=[chatbot],
    additional_outputs=[chatbot],
)
logger.info("Gradio interface configured successfully")

# Mount the stream to the FastAPI app
logger.info("Mounting stream to FastAPI application...")
stream.mount(app)
logger.info("Stream mounted successfully")


@app.get("/")
async def root():
    """Serve the main HTML page"""
    logger.info("Serving main HTML page")
    html_content = (Path(__file__).parent / "index.html").read_text()
    # Replace system prompt placeholder
    html_content = html_content.replace("__SYSTEM_PROMPT__", SYSTEM_PROMPT)
    logger.debug("HTML content loaded and system prompt injected successfully")
    return HTMLResponse(content=html_content)


@app.post("/process_audio")
async def process_audio_endpoint(file: UploadFile = File(...)):
    """Handle audio processing from the frontend"""
    logger.info("Received audio file for processing")
    try:
        # Read the audio file
        audio_data = await file.read()
        logger.debug(f"Read {len(audio_data)} bytes of audio data")

        # Print first 20 printable characters for debugging
        printable_chars = "".join(chr(b) if 32 <= b <= 126 else "." for b in audio_data[:20])
        logger.debug(f"First 20 bytes (printable): {printable_chars}")
        logger.debug(f"First 20 bytes (hex): {' '.join(f'{b:02x}' for b in audio_data[:20])}")

        # Try to read as WAV file
        try:
            with wave.open(io.BytesIO(audio_data), "rb") as wav_file:
                # Get WAV parameters
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                n_frames = wav_file.getnframes()

                logger.debug(
                    f"WAV parameters: channels={n_channels}, sample_width={sample_width}, frame_rate={frame_rate}, frames={n_frames}"
                )

                # Read all frames
                frames = wav_file.readframes(n_frames)

                # Convert to numpy array based on sample width
                if sample_width == 2:  # 16-bit
                    audio_array = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
                elif sample_width == 4:  # 32-bit
                    audio_array = np.frombuffer(frames, dtype=np.float32)
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")

                # Handle multiple channels
                if n_channels > 1:
                    audio_array = audio_array.reshape(-1, n_channels)
                    # Convert to mono by averaging channels
                    audio_array = np.mean(audio_array, axis=1)

                logger.debug(f"Converted WAV to array with shape {audio_array.shape} and dtype {audio_array.dtype}")

        except wave.Error as e:
            logger.debug(f"Not a WAV file: {str(e)}, trying direct conversion")
            # Fall back to direct conversion if not a WAV file
            try:
                audio_array = np.frombuffer(audio_data, dtype=np.float32)
                logger.debug("Successfully converted to float32 array")
            except ValueError as e:
                logger.debug(f"Float32 conversion failed: {str(e)}, trying int16")
                try:
                    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                    logger.debug("Successfully converted to int16 array")
                except ValueError as e:
                    logger.error(f"All conversion attempts failed: {str(e)}")
                    raise HTTPException(status_code=400, detail=f"Invalid audio format: {str(e)}")

        # Ensure the array is 1D
        if len(audio_array.shape) > 1:
            audio_array = audio_array.flatten()
            logger.debug(f"Flattened array to shape {audio_array.shape}")

        # Create audio tuple with proper sample rate
        audio_tuple = (AUDIO_SAMPLE_RATE, audio_array)
        logger.debug(f"Created audio tuple with sample rate {AUDIO_SAMPLE_RATE} and array shape {audio_array.shape}")

        # Process the audio
        try:
            audio_response, chat_history = process_audio(audio_tuple)
            logger.debug("Audio processing completed successfully")
        except Exception as e:
            logger.error(f"Error in process_audio: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

        # Convert audio response to bytes
        try:
            response_audio_bytes = audio_to_bytes(audio_response)
            logger.debug(f"Converted response audio to {len(response_audio_bytes)} bytes")
        except Exception as e:
            logger.error(f"Error converting response audio to bytes: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error converting response audio: {str(e)}")

        # Get the last message from chat history
        last_message = chat_history[-1]["content"] if chat_history else ""

        return JSONResponse({"text": last_message, "audio": response_audio_bytes.hex()})  # Convert bytes to hex string for JSON
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting application on port {UVICORN_PORT} (development mode: {DEVELOPMENT_MODE})")
    uvicorn.run("talk_to_ollama:app", host="0.0.0.0", port=UVICORN_PORT, reload=DEVELOPMENT_MODE)
