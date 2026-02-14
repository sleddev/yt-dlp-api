import json
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from yt_dlp import YoutubeDL

app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/info")
def get_video_info(url: str):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        return(ydl.sanitize_info(info))


@app.get("/download")
def get_video(url: str):
    ydl_opts = {}

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        path = os.path.join(os.path.curdir, "downloads", info.get("id"))
        os.makedirs(path, exist_ok=True)

        ydl_opts = {
            "outtmpl": os.path.join(path, "%(title)s.%(ext)s")
        }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    with open(os.path.join(path, "info.json"), "w", encoding="utf8") as f:
        json.dump(info, f)

    files = os.listdir(path)
    downloaded_name = [
        f for f in files
        if not f.endswith(".json") and not os.path.isdir(os.path.join(path, f))
    ][0]

    return FileResponse(os.path.join(path, downloaded_name))