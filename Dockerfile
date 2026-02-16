FROM python:3.14-slim

RUN pip install --no-cache-dir uv

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl unzip xz-utils && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz -o ffmpeg.tar.xz && \
    mkdir ffmpeg_temp && \
    tar -xJ -f ffmpeg.tar.xz -C ffmpeg_temp --strip-components=1 && \
    mv ffmpeg_temp/bin/ffmpeg /usr/local/bin/ && \
    mv ffmpeg_temp/bin/ffprobe /usr/local/bin/ && \
    chmod a+rx /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf ffmpeg.tar.xz ffmpeg_temp

RUN sh -c "curl -fsSL https://deno.land/install.sh | sh"
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-dev

COPY . .

RUN mkdir -p downloads

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
