#!/usr/bin/env python3
import pychromecast, requests, praw, time, os
from pychromecast.controllers.youtube import YouTubeController

CAST_NAME = "Living Room TV"

# Change to the video id of the YouTube video
# video id is the last part of the url http://youtube.com/watch?v=video_id
VIDEO_ID = "Jwtn5_d2YCs"
played_yet = False


chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == CAST_NAME)
cast.wait()
yt = YouTubeController()
cast.register_handler(yt)
reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                    client_secret=os.getenv("CLIENT_SECRET"),
                    username=os.getenv("REDDIT_USERNAME"), 
                    password=os.getenv("REDDIT_PASSWORD"),
                    user_agent="youtube_haiku_bot")
for submission in reddit.subreddit('youtubehaiku').hot(limit=25):
    link = submission.url
    VIDEO_ID = ""
    if "youtu.be" in link:
        # resolve youtu.be urls
        r = requests.get(link)
        link = r.url
    if "youtube.com" in link:
        v_spot = link.find("v=")
        just_params = link[v_spot+2:]
        VIDEO_ID = just_params
        amp = VIDEO_ID.find("&")
        if amp != -1:
            VIDEO_ID = VIDEO_ID[:amp]
    if VIDEO_ID != "":
        if played_yet:
            yt.add_to_queue(VIDEO_ID)
        else:
            played_yet = True
            yt.play_video(VIDEO_ID)
        print(VIDEO_ID)
# Change to the name of your Chromecast
