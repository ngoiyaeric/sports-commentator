import cv2  # We're using OpenCV to read video, to install use: !pip install opencv-python
import base64
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client with the API key

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))


# Load the video
video = cv2.VideoCapture("./match.mp4")

# Read frames from the video and encode them to base64
base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()
print(len(base64Frames), "frames read.")

# Prepare the prompt messages
PROMPT_MESSAGES = [
    {
        "role": "system",
        "content": "You are a live soccer commentator. Identify the teams playing from the visual content of the match and refer to them by their names in your commentary. Keep track of each event, players involved, play time and score"
    },
    {
        "role": "user",
        "content": "You are a live soccer commentator for an intense and thrilling match. Your job is to provide vivid and engaging play-by-play commentary, capturing every moment with great detail and enthusiasm. Describe the actions, emotions, strategies, and key moments of the match. Make sure to include player names, positions, and any notable statistics or background information that adds depth to the commentary. Your commentary should make the listener feel like they are right there in the stadium, experiencing the game with all its excitement and tension."
    },
    {
        "role": "user",
        "content": [
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::20]),  # Sampling every 20th frame
        ],
    }
]

# This code snippet is using the OpenAI API to generate a compelling soccer commentary based on the
# frames extracted from a soccer match video.
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 16384,
}

# Get the response from OpenAI API
result = client.chat.completions.create(**params)

commentary = result.choices[0].message['content']
print(commentary)

# Generate audio from the commentary
response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    },
    json={
        "model": "tts-1-1106",
        "input": commentary,
        "voice": "onyx",
    },
)

# Collect the audio data
audio = b""
for chunk in response.iter_content(chunk_size=1024 * 1024):
    audio += chunk

# Save the audio to a file or process it further
with open("commentary_audio.mp3", "wb") as audio_file:
    audio_file.write(audio)

# Optionally, you can play the audio in a Jupyter environment
# from IPython.display import Audio
# Audio(audio)
