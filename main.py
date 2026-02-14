import json
from fastapi import FastAPI
from yt_dlp import YoutubeDL

app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/video-info")
def get_video_info(url: str):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        return(ydl.sanitize_info(info))


@app.get("/video")
def get_video(url: str):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.download([url])

        return(ydl.sanitize_info(info))