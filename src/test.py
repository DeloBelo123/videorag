from flow import turn_link_to_rag

turn_link_to_rag(
    link="https://www.youtube.com/watch?v=-7iGhc4pZcg",
    screenshot_timestamps=["00:00:00", "00:01:00", "00:02:00"],
    video_title="testing a new clash-royale deck",
    video_topic="the video is about ken who plays a new clash-royale deck for the first time in competition and is testing the decks features",
    include_summarizer=True
)