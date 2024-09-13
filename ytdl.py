import yt_dlp as yt
import os

class YoutubeDownloader:
    def __init__(self, output_dir="data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def download_video(self, url, quality='360p', audio_only=False, subtitles=True):
        ydl_opts = {
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'nocheckcertificate': True,
            'writesubtitles': subtitles,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'vtt' if subtitles else None,
            'embedsubtitles': subtitles,
            'noprogress': True,
            'nooverwrites': False,
            'continuedl': False,
            'nopart': True,
        }

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                    {'key': 'FFmpegMetadata'},
                ],
                'merge_output_format': 'mp3',
            })
        else:
            video_format = {
                '360p': 'b:360p/best',
                '720p': 'b:720p/best',
                '1080p': 'bestvideo[height=1080]+bestaudio/best',
            }.get(quality, 'bestvideo[height=1080]+bestaudio/best')

            ydl_opts.update({
                'format': video_format,
                'merge_output_format': 'mp4',
                'postprocessors': [
                    {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                    {'key': 'FFmpegMetadata'},
                    {'key': 'FFmpegEmbedSubtitle'} if subtitles else {},
                ],
            })

        try:
            with yt.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "Untitled")
                file_ext = 'mp3' if audio_only else 'mp4'
                file_path = os.path.join(self.output_dir, f"{title}.{file_ext}")
                return os.path.abspath(file_path), title
        except Exception as e:
            raise RuntimeError(f"Download error: {e}")

    def stream_video(self, url, quality='360p', audio_only=False, subtitles=True):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'writesubtitles': subtitles,
            'subtitleslangs': ['en'],
            'format': 'bestaudio/best' if audio_only else f'bestvideo[height={quality}]+bestaudio/best',
        }

        try:
            with yt.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                if audio_only:
                    stream_url = next(f['url'] for f in formats if f.get('acodec') != 'none')
                else:
                    stream_url = next(f['url'] for f in formats if f.get('format_note') == quality and f.get('vcodec') != 'none')

                title = info.get("title", "Untitled")
                return stream_url, title
        except Exception as e:
            raise RuntimeError(f"Stream URL error: {e}")

    def get_video_info(self, url):
        ydl_opts = {'quiet': True, 'skip_download': True}

        try:
            with yt.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get('title', 'Unknown'),
                    "description": info.get('description', 'No description'),
                    "upload_date": info.get('upload_date', 'Unknown')
                }
        except Exception as e:
            return {"error": f"Error: {e}"}
