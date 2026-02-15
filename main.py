import json
import os
import dotenv
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from yt_dlp import YoutubeDL

dotenv.load_dotenv()
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
def get_video(url: str, password: str, setfilename: bool = True):
    ydl_opts = {
        "cookiefile": "/app/cookies.txt",
    }

    if password != os.environ.get("DOWNLOAD_PASS"):
        return Response(status_code=401)

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        path = os.path.join(os.path.curdir, "downloads", info.get("id"))
        os.makedirs(path, exist_ok=True)

        ydl_opts.update({
            "outtmpl": os.path.join(path, "%(title)s.%(ext)s")
        })

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    with open(os.path.join(path, "info.json"), "w", encoding="utf8") as f:
        json.dump(info, f)

    files = os.listdir(path)
    downloaded_name = [
        f for f in files
        if not f.endswith(".json") and not os.path.isdir(os.path.join(path, f))
    ][0]

    return FileResponse(os.path.join(path, downloaded_name), filename=downloaded_name if setfilename else None)