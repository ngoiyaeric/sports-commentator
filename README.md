# Sports-commentator
 GPT Sports commentator

This script uses OpenCV and OpenAI's API to generate live sports commentary based on a video of a sport match. It reads the video frames, processes them, and creates an engaging play-by-play commentary. The commentary is then converted to audio and saved as an MP3 file.

Prerequisites
Python 3.7 or higher
OpenCV
OpenAI API key
Requests library
dotenv library
Installation
Clone the repository or download the script.

Install the required libraries:

sh
Copy code
pip install opencv-python requests python-dotenv
Set up your OpenAI API key:

Create a .env file in the same directory as the script.
Add your OpenAI API key to the .env file:
makefile
Copy code
OPENAI_API_KEY=your_openai_api_key
Ensure you have a video file named match.mp4 in the same directory as the script or update the script with the correct path to your video file.

Usage
Run the script:

sh
Copy code
python sports_commentator.py
The script performs the following steps:

Loads the video file.
Reads frames from the video and encodes them to base64.
Prepares the prompt messages for the OpenAI API.
Sends the prompts to the OpenAI API to generate the commentary.
Receives the generated commentary and converts it to audio using the OpenAI API.
Saves the audio commentary as commentary_audio.mp3

# Adjustments: 
Vary the frame sampling frequency based on the speed of the sports, sample more frequently ie 20 frames instead of 50 for basketball instead of soccer. Experiment with this for gpt-4o commentary resolution. 


