import httpx
import shlex
import os
import base64
import subprocess
from faster_whisper import WhisperModel
from typing import List

from dotenv import load_dotenv
load_dotenv()

llm_apikey = os.getenv("OPENROUTER_API_KEY")
if not llm_apikey:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

def cli_exec(command:str):
    try:
        command_arr = shlex.split(command)
        subprocess.run(command_arr, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command {command_arr}: {e}")
        return False

def hhmmss_to_seconds(timestamp: str) -> float:
    h, m, s = map(int, timestamp.split(":"))
    return h * 3600 + m * 60 + s

#image encoding
def turn_link_to_video(link:str,video_output_path:str):
    cli_exec(f'yt-dlp -f bestvideo+bestaudio -o "{video_output_path}" "{link}"')

def take_screenshot(video_path:str,output_path:str,timestamp:float):
    cli_exec(f'ffmpeg -ss {timestamp} -i "{video_path}" -frames:v 1 "{output_path}"')

def encode_image(path:str) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def llm_describe_image(image_path:str):
    try:
        img_b64 = encode_image(image_path)
        response = httpx.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {llm_apikey}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe objectively what is visible in this image."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_b64}"
                                }
                            }
                        ]
                    }
                ]
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error describing image {image_path}: {e}")
        return None

def llm_describe_images(image_paths:List[str]):
    descriptions = ""
    for i, image_path in enumerate(image_paths,start=1):
        descriptions += f"Picture {i}: {llm_describe_image(image_path)}\n"
    return descriptions

#speech 
def turn_link_to_speech(link:str,audio_output_path:str):
    cli_exec(f'yt-dlp -f bestaudio -x --audio-format mp3 -o "{audio_output_path}" "{link}"')

model = WhisperModel("small", device="cpu")
def speech_to_text(audio_path:str):
    segments, info = model.transcribe(audio_path)
    content = [f"[{segment.start:.2f} → {segment.end:.2f}] {segment.text}" for segment in segments]
    return content
