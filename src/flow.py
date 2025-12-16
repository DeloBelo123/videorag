from file_utils import create_file,read_file,add_to_file,does_file_exist
from setup import turn_link_to_video,take_screenshot,llm_describe_image,speech_to_text,turn_link_to_speech,hhmmss_to_seconds,summarizer

def turn_link_to_rag(
    link:str, 
    video_title:str = None,
    video_topic:str = None,
    fokuss_in_summary:str = None,
    ignore_in_pictures:str = None,
    screenshot_timestamps:list[str] = None,#in Form 'HH:MM:SS'
    rag_output_path:str = "video_rag.txt",
    video_output_path:str = "video.mp4",
    audio_output_path:str = "audio.mp3",
    include_summarizer:bool = False
):
    real_video_title = f"VIDEO TITLE: {video_title}\n" if video_title else "Unknown"
    real_video_topic = f"VIDEO TOPIC: {video_topic}\n" if video_topic else "Unknown"

    # video und audio datein erstellen
    if not turn_link_to_video(link,video_output_path):
        raise RuntimeError(f"Video-Download fehlgeschlagen: {link}")
    
    if not turn_link_to_speech(link,audio_output_path,video_output_path):
        raise RuntimeError(f"Audio-Download fehlgeschlagen: {link}")

    #prüfen ob die rag datei exestiert, wenn nein erstellen wir die
    if not does_file_exist(rag_output_path):
        create_file(rag_output_path,f"VIDEO RAG:\n{real_video_title}{real_video_topic}")
    
    #prüfen ob audio datei existiert
    if not does_file_exist(audio_output_path):
        raise RuntimeError(f"Audio-Datei '{audio_output_path}' wurde nicht erstellt")
    
    #prüfen ob video datei existiert
    if not does_file_exist(video_output_path):
        raise RuntimeError(f"Video-Datei '{video_output_path}' wurde nicht erstellt")
    
    #die audio aud dem video rausholen
    text = "\n".join(speech_to_text(audio_output_path))

    #das visuelle aus dem video rausholen
    if screenshot_timestamps:
        screenshot_paths = []
        for i,timestamp in enumerate(screenshot_timestamps,start=1):
            take_screenshot(video_output_path,f"screenshot_{i}.jpg",hhmmss_to_seconds(timestamp))
            screenshot_paths.append(f"screenshot_{i}.jpg")
        descriptions = llm_describe_image(screenshot_paths,video_title,video_topic,ignore_in_pictures)

    #die datein jetzt in die Datei einfügen
    if include_summarizer:
        add_to_file(rag_output_path,summarizer(f"SUMMARY:\n{text}",video_title,video_topic,fokuss_in_summary))
    add_to_file(rag_output_path,f"WORD FOR WORDTRANSCRIPT:\n{text}")
    if screenshot_timestamps:
        add_to_file(rag_output_path,f"VISUAL DESCRIPTION:\n{descriptions}")
    return rag_output_path