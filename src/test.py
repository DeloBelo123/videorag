from flow import turn_link_to_rag

turn_link_to_rag(
    link="https://www.youtube.com/watch?v=K-OCUDYpnj4",
    screenshot_timestamps=["00:00:02","00:02:20","00:04:25","00:05:07","00:07:24","00:08:38","00:10:47","00:12:27","00:14:01"],
    video_title="How To Grow Taller After Puberty: Full Microfracture Guide (with real-life examples)",
    video_topic="The video is about how to grow taller after puberty",
    include_summarizer=True,
    fokuss_in_summary="on the data and information said in the video about bone-growth and the microfractures",
)