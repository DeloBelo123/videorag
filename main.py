from flow import turn_link_to_rag
from typing import Optional
import re

def check_timestamps(timestamps:str):
    regex = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$')
    if not regex.match(timestamps):
        return False
    return True

def main():
    yt_link = input("von Welchem Video wollen sie RAG haben?\n Eingabe: ")
    screenshot_timestamps = input('''
    in welchen minuten willst du screenshots? bitte in Form 'HH:MM:SS' angeben und nur mit Komma trennen (kein Leerzeichen)\n
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
    turn_link_to_rag(
        link=yt_link,
        screenshot_timestamps=real_screenshots_timestamps,
        rag_output_path=final_name
    )
    print(f"RAG Datei wurde erfolgreich generiert und ist unter {final_name} zu finden")

if __name__ == "__main__":
    main()