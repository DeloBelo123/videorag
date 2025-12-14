from file_utils import create_file,read_file,add_to_file,does_file_exist
from setup import turn_link_to_video,take_screenshot,llm_describe_image,speech_to_text,turn_link_to_speech,hhmmss_to_seconds

def turn_link_to_rag(
    link:str,
    screenshot_timestamps:list[str], #in Form 'HH:MM:SS'
    rag_output_path:str = "video_rag.txt",
    video_output_path:str = "video.mp4",
    audio_output_path:str = "audio.mp3"
):
    # video und audio datein erstellen
    turn_link_to_video(link,video_output_path)
    turn_link_to_speech(link,audio_output_path)

    #prüfen ob die rag datei exestiert, wenn nein erstellen wir die
    if not does_file_exist(rag_output_path):
        create_file(rag_output_path,"")
    
    #die audio aud dem video rausholen
    text = "\n".join(speech_to_text(audio_output_path))

    #das visuelle aus dem video rausholen
    descriptions = ""
    for i,timestamp in enumerate(screenshot_timestamps,start=1):
        take_screenshot(video_output_path,f"screenshot_{i}.jpg",hhmmss_to_seconds(timestamp))
        descriptions += f"[IMAGE {i}] {llm_describe_image(f'screenshot_{i}.jpg')}\n"

    #die datein jetzt in die Datei einfügen
    add_to_file(rag_output_path,text)
    add_to_file(rag_output_path,descriptions)
    return rag_output_path