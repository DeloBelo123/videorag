from video_flow import turn_video_to_rag
from typing import Optional
import re

def check_timestamps(timestamps:str):
    time_regex = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$')
    if not time_regex.match(timestamps):
        return False
    return True

def is_valid_link(s: str) -> bool:
    url_regex = re.compile(
    r'^(?:(?:https?://)|(?:www\.))'        
    r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'      
    r'(?::\d{2,5})?'                         
    r'(?:/[^\s]*)?$',                        
    re.IGNORECASE
)
    return bool(url_regex.fullmatch(s.strip()))

def main():
    yt_link = input("\nvon Welchem Video wollen sie RAG haben?\nLink Eingabe: ")
    if not is_valid_link(yt_link):
        print("falsche eingabe, sie müssen einen gültigen Link eingeben")
        return
    video_title = input("\nVideo Title Eingabe: ")
    video_topic = input("\nVideo Thema Eingabe: ")
    screenshot_timestamps = input('''\nin welchen minuten willst du screenshots? bitte in Form 'HH:MM:SS' angeben und nur mit Komma trennen (kein Leerzeichen)\n
    Beispiel: '00:03:25,00:05:22,00:08:49'\n
    Eingabe: 
    ''')
    for timestamp in screenshot_timestamps.split(","):
        if not check_timestamps(timestamp):
            print("falsche eingabe, sie müssen in Form 'HH:MM:SS' eingeben")
            return
    real_screenshots_timestamps = [timestamp for timestamp in screenshot_timestamps.split(",")] 
    rag_file_name:Optional[str] = input("(optional) wie soll die generierte Datei heissen? Wenns nicht juckt, einfach Enter drücken")
    final_name = rag_file_name if rag_file_name else "video_rag.txt"
    turn_video_to_rag(
        link=yt_link,
        screenshot_timestamps=real_screenshots_timestamps,
        rag_output_path=final_name,
        video_title=video_title,
        video_topic=video_topic,
        include_summarizer=True
    )
    print(f"RAG Datei wurde erfolgreich generiert und ist unter {final_name} zu finden")

if __name__ == "__main__":
    main()