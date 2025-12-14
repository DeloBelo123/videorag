from file_utils import create_file,read_file,add_to_file,does_file_exist
from setup import turn_link_to_video,take_screenshot,llm_describe_image,speech_to_text,turn_link_to_speech,hhmmss_to_seconds,summarizer

def turn_link_to_rag(
    link:str,
    screenshot_timestamps:list[str], #in Form 'HH:MM:SS'
    video_title:str,
    video_topic:str,
    rag_output_path:str = "video_rag.txt",
    video_output_path:str = "video.mp4",
    audio_output_path:str = "audio.mp3",
    include_summarizer:bool = False
):
    # video und audio datein erstellen
    if not turn_link_to_video(link,video_output_path):
        raise RuntimeError(f"Video-Download fehlgeschlagen: {link}")
    
    if not turn_link_to_speech(link,audio_output_path,video_output_path):
        raise RuntimeError(f"Audio-Download fehlgeschlagen: {link}")

    #prüfen ob die rag datei exestiert, wenn nein erstellen wir die
    if not does_file_exist(rag_output_path):
        create_file(rag_output_path,f"VIDEO RAG:\nVideo Title: {video_title}\nVideo Topic: {video_topic}\n")
    
    #prüfen ob audio datei existiert
    if not does_file_exist(audio_output_path):
        raise RuntimeError(f"Audio-Datei '{audio_output_path}' wurde nicht erstellt")
    
    #prüfen ob video datei existiert
    if not does_file_exist(video_output_path):
        raise RuntimeError(f"Video-Datei '{video_output_path}' wurde nicht erstellt")
    
    #die audio aud dem video rausholen
    text = "\n".join(speech_to_text(audio_output_path))

    #das visuelle aus dem video rausholen
    screenshot_paths = []
    for i,timestamp in enumerate(screenshot_timestamps,start=1):
        take_screenshot(video_output_path,f"screenshot_{i}.jpg",hhmmss_to_seconds(timestamp))
        screenshot_paths.append(f"screenshot_{i}.jpg")
    descriptions = llm_describe_image(screenshot_paths,video_title,video_topic)

    #die datein jetzt in die Datei einfügen
    if include_summarizer:
        add_to_file(rag_output_path,summarizer(f"SUMMARY:\n{text}",video_title,video_topic))
    add_to_file(rag_output_path,f"WORD FOR WORDTRANSCRIPT:\n{text}")
    add_to_file(rag_output_path,f"VISUAL DESCRIPTION:\n{descriptions}")
    return rag_output_path