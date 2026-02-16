import json
import os
import dotenv
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from yt_dlp import YoutubeDL

dotenv.load_dotenv()

cookies_path = os.environ.get("COOKIES_PATH") if os.path.isabs(os.environ.get("COOKIES_PATH")) else os.path.join(os.path.curdir, os.environ.get("COOKIES_PATH"))
cookies_content = os.environ.get("COOKIES_TXT")
if cookies_content:
    with open(cookies_path, "w", encoding="utf-8") as f:
        f.write(cookies_content)

app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/info")
def get_video_info(url: str):
    ydl_opts = {
        "cookiefile": cookies_path,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        return(ydl.sanitize_info(info))


@app.get("/download")
def get_video(url: str, password: str, setfilename: bool = True):
    ydl_opts = {
        "cookiefile": cookies_path,
        "outtmpl": os.path.join(os.path.curdir, "downloads", "%(id)s", "%(title)s.%(ext)s"),
        "remote_components": ["ejs:github","ejs:npm"],
    }

    if password != os.environ.get("DOWNLOAD_PASS"):
        return Response(status_code=401)

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        sanitized = ydl.sanitize_info(info)

    path = os.path.join(os.path.curdir, "downloads", info.get("id"))

    with open(os.path.join(path, "info.json"), "w", encoding="utf8") as f:
        json.dump(sanitized, f)

    files = os.listdir(path)
    downloaded_name = [
        f for f in files
        if not f.endswith(".json") and not os.path.isdir(os.path.join(path, f))
    ][0]

    return FileResponse(os.path.join(path, downloaded_name), filename=downloaded_name if setfilename else None)