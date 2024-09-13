from flask import Flask, request, send_file, abort, redirect
from ytdl import YoutubeDownloader
import time
import os

app = Flask(__name__)
downloader = YoutubeDownloader()

@app.route("/")
def index():
    return "YouTube Downloader API"

@app.route('/watch', methods=["GET"])
def watch_video():
    video_id = request.args.get("v")
    quality = request.args.get("q", "360p")
    subtitles = request.args.get("sub", "true").lower() == "true"
    media_type = request.args.get("media", "mp4")

    if not video_id:
        abort(400, description="Missing video ID")

    url = f"https://youtube.com/watch?v={video_id}"
    audio_only = media_type.lower() == "mp3"

    try:
        if quality == "1080p" or audio_only:
            file_path, title = downloader.download_video(url, quality=quality, audio_only=audio_only, subtitles=subtitles)
        else:
            stream_url, title = downloader.stream_video(url, quality=quality, audio_only=audio_only, subtitles=subtitles)
            return redirect(stream_url, code=302)
    except Exception as e:
        abort(500, description=f"Error: {e}")

    max_attempts, wait_time = 5, 0.3
    for _ in range(max_attempts):
        if os.path.isfile(file_path):
            break
        time.sleep(wait_time)
        wait_time *= 2
    else:
        abort(404, description="File not found after download")

    file_ext = 'mp3' if audio_only else 'mp4'
    download_name = f"{title}.{file_ext}"

    response = send_file(file_path, as_attachment=True, download_name=download_name)
    response.headers['X-Title'] = title
    response.headers['X-Message'] = "Download successful"

    if quality == "1080p" or audio_only:
        os.remove(file_path)

    return response

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=6969)
