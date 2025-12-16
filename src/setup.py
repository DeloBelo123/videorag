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
    formats = ["best", "bestvideo+bestaudio", "worst"]
    for fmt in formats:
        if cli_exec(f'yt-dlp --no-playlist -f "{fmt}" -o "{video_output_path}" "{link}"'):
            return True
    return False

def take_screenshot(video_path:str,output_path:str,timestamp:float):
    cli_exec(f'ffmpeg -ss {timestamp} -i "{video_path}" -frames:v 1 "{output_path}"')

def encode_image(path:str) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def llm_describe_image(image_paths:list[str],video_title:str,video_description:str):
    try:
        content = [
            {
                "type": "text",
                "text": f"""
            You are a professional video scene analyst.

            You are given MULTIPLE screenshots taken from the SAME video.
            The screenshots are ordered CHRONOLOGICALLY from earlier to later.

            VIDEO TITLE:
            {video_title}

            VIDEO DESCRIPTION:
            {video_description}

            TASK:
            - Interpret the screenshots as PARTS OF A CONTINUOUS VIDEO.
            - Do NOT describe each image in isolation.
            - Identify recurring people, objects, or UI elements across screenshots.
            - Describe how the scene, actions, or context EVOLVE over time.
            - Use the video topic to infer meaning (e.g. gameplay progression, commentary, reactions).
            - Be concise, structured, and RAG-friendly.
            - IMPORTANT: when seeing charts, tables, graphs oder statistics, describe them fully and accurately, in a way that is RAG friendly and can be used to answer questions about the video.
            - Focus on the topic of the video

            OUTPUT:
            Write a coherent visual summary that explains what is happening visually in the video.
            """
                        }
                    ]
        # Bilder anhängen (in Reihenfolge!)
        for img_path in image_paths:
            img_b64 = encode_image(img_path)
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_b64}"
                    }
                }
            )

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
                        "content": content
                    }
                ]
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Error describing video screenshots: {e}")
        return None

#speech 
def turn_link_to_speech(link:str,audio_output_path:str,video_path:str=None):
    formats = ["bestaudio", "worstaudio"]
    for fmt in formats:
        if cli_exec(f'yt-dlp --no-playlist -f "{fmt}" -x --audio-format mp3 -o "{audio_output_path}" "{link}"'):
            return True
    
    if video_path and os.path.exists(video_path):
        if cli_exec(f'ffmpeg -i "{video_path}" -vn -acodec libmp3lame -ab 192k "{audio_output_path}"'):
            return True
    
    return False

model = WhisperModel("small", device="cpu")
def speech_to_text(audio_path:str):
    segments, info = model.transcribe(audio_path)
    content = [f"[{segment.start:.2f} → {segment.end:.2f}] {segment.text}" for segment in segments]
    return content

# AI summarizer
def summarizer(text:str,video_title:str,video_topic:str,fokuss:str = None):
    real_focus = f"when summarizing, focus espacialy on the following topic: {fokuss}" if fokuss else ""
    prompt = f"""
        You are a professional video content analyst specialized in creating
        high-quality summaries for Retrieval-Augmented Generation (RAG) systems.

        You are given the FULL transcript of a video as plain text.
        Each line begins with a timestamp in the format:
        [START → END] spoken text

        VIDEO TITLE: "{video_title}"
        VIDEO TOPIC: "{video_topic}"

        {real_focus}

        YOUR TASK:
        1. Split the video into meaningful, semantic CHAPTERS.
        2. Each chapter must represent a coherent idea, phase, or topic in the video.
        3. Focus on the topic of the video and the data said
        4. For EACH chapter, provide:
        - A clear, descriptive TITLE (RAG-friendly, informative, specific)
        - The EXACT TIME RANGE using the original timestamps
        - A detailed SUMMARY that explains what is happening or being discussed

        IMPORTANT RULES:
        - Do NOT include or repeat the original transcript text.
        - Do NOT invent timestamps.
        - Use only timestamps that appear in the input.
        - Chapters must be in chronological order.
        - Summaries should be concise but information-dense.
        - Write summaries so that someone can understand the video without watching it.
        - The transcript may be VERY LONG — handle it fully.

        OUTPUT FORMAT (STRICT):

        [CHAPTER X]
        TITLE: ...
        RANGE: [start → end]
        SUMMARY:
        ...
"""

    response = httpx.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {llm_apikey}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]