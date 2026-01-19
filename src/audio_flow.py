from file_utils import create_file, add_to_file, does_file_exist
from setup import turn_link_to_speech, speech_to_text, summarizer


def turn_audio_to_rag(
    link: str,
    podcast_title: str = None,
    podcast_topic: str = None,
    fokus_in_summary: str = None,
    rag_output_path: str = "podcast_rag.txt",
    audio_output_path: str = "audio.mp3",
    include_summarizer: bool = False
):
    """
    Audio-only RAG pipeline for podcasts.
    - Downloads audio from URL
    - Transcribes word-for-word
    - Optionally summarizes
    - NO video logic, NO screenshots, NO visual analysis
    """

    real_title = f"PODCAST TITLE: {podcast_title}\n" if podcast_title else "PODCAST TITLE: Unknown\n"
    real_topic = f"PODCAST TOPIC: {podcast_topic}\n" if podcast_topic else "PODCAST TOPIC: Unknown\n"

    # 🎧 Audio extrahieren (Podcast-safe)
    if not turn_link_to_speech(link, audio_output_path):
        raise RuntimeError(f"Audio-Download fehlgeschlagen: {link}")

    # 📄 RAG-Datei anlegen, falls nicht vorhanden
    if not does_file_exist(rag_output_path):
        create_file(
            rag_output_path,
            f"PODCAST RAG:\n{real_title}{real_topic}"
        )

    # 🔍 Audio-Datei prüfen
    if not does_file_exist(audio_output_path):
        raise RuntimeError(f"Audio-Datei '{audio_output_path}' wurde nicht erstellt")

    # 📝 Wort-für-Wort-Transkript
    transcript_segments = speech_to_text(audio_output_path)
    transcript_text = "\n".join(transcript_segments)

    # 🧠 Optional: semantische Zusammenfassung
    if include_summarizer:
        summary = summarizer(
            text=f"SUMMARY:\n{transcript_text}",
            video_title=podcast_title,
            video_topic=podcast_topic,
            fokuss=fokus_in_summary
        )
        add_to_file(rag_output_path, summary)

    # 📚 Roh-Transkript immer speichern
    add_to_file(
        rag_output_path,
        f"WORD FOR WORD TRANSCRIPT:\n{transcript_text}"
    )

    return rag_output_path
