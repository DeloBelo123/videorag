from setup import  llm_describe_image
from file_utils import read_file

image_paths = ["screenshot_1.jpg", "screenshot_2.jpg", "screenshot_3.jpg"]
video_title = "testing a new clash-royale deck"
video_description = "the video is about ken who plays a new clash-royale deck for the first time in competition and ist testing the decks features"
print(llm_describe_image(image_paths,video_title,video_description))

