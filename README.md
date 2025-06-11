# YouTube Downloader API

This Flask application provides an API to download YouTube videos or retrieve direct streamable links.

## Features

- Download videos in various qualities (360p, 720p, 1080p).
- Download audio-only in MP3 format.
- Get direct streamable links for certain video qualities.
- Option to include subtitles (embedded in downloaded video).

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- `yt-dlp`: For downloading video/audio and extracting information.
- `ffmpeg`: For video/audio processing (e.g., merging formats, extracting audio, embedding subtitles).

## Setup and Installation

1.  **Clone the repository (if applicable) or download the files.**

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    Ensure `ffmpeg` is installed on your system and accessible in your PATH. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

## Running the Application

There are several ways to run the application:

### 1. Development Server (for testing on your local machine)

   This method is suitable for development and testing. It will typically run the server on `http://127.0.0.1:6969` or `http://localhost:6969`.

   ```bash
   python app.py
   ```

### 2. Production Server with Gunicorn (Recommended for deployment)

   Gunicorn is a robust WSGI HTTP server for UNIX. It's recommended for production deployments.

   **To run on your private network (accessible by other devices on the same network):**

   Use `0.0.0.0` as the host to make the server listen on all available network interfaces.

   ```bash
   gunicorn app:app --bind 0.0.0.0:8000
   ```

   -   `app:app`: Refers to the Flask application instance (`app`) in your `app.py` file.
   -   `--bind 0.0.0.0:8000`: Makes the server listen on port 8000 on all network interfaces. You can access it from other devices on your network using your machine's private IP address (e.g., `http://192.168.1.10:8000`).
   -   You can use asynchronous workers for better performance with I/O-bound tasks like downloads:
       ```bash
       pip install gevent
       gunicorn app:app --bind 0.0.0.0:8000 --worker-class gevent --workers 4
       ```

## API Documentation

Once the server is running, you can access the API documentation (which serves as the landing page) in your browser at the root URL:

-   If running with `python app.py` (default port 6969): `http://localhost:6969/`
-   If running with Gunicorn on port 8000: `http://<your-server-ip>:8000/`

## Exposing to the Internet with Cloudflare Tunnel (Port Forwarding Alternative)

Instead of traditional port forwarding (which can have security implications and require router configuration), you can use Cloudflare Tunnel (formerly Argo Tunnel) to securely expose your local server to the internet.

**Benefits of Cloudflare Tunnel:**

-   No need to open ports on your router/firewall.
-   Traffic is proxied through Cloudflare's network, providing DDoS protection and SSL.
-   You can use a custom domain or a free `trycloudflare.com` subdomain.

**Steps:**

1.  **Sign up for a Cloudflare account** (if you don't have one) and add your domain (optional, you can use a free subdomain).

2.  **Install `cloudflared`:**
    Follow the instructions for your OS on the [Cloudflare documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/).

3.  **Log in `cloudflared` to your Cloudflare account:**
    ```bash
    cloudflared login
    ```
    This will open a browser window to authorize `cloudflared`.

4.  **Create and run a tunnel:**

    *   **For a quick test with a random subdomain:**
        Assuming your Flask app (via Gunicorn) is running on `localhost:8000`:
        ```bash
        cloudflared tunnel --url localhost:8000
        ```
        `cloudflared` will output a URL like `https://<random-words>.trycloudflare.com` that you can use to access your API from anywhere.

    *   **For a persistent tunnel with a custom domain or a named free subdomain:**

        a.  **Create a tunnel:**
            ```bash
            cloudflared tunnel create my-youtube-api-tunnel
            ```
            This will output a Tunnel ID and create a credentials file.

        b.  **Configure DNS (if using your own domain):**
            Create a CNAME record in your Cloudflare DNS settings pointing your desired subdomain (e.g., `api.yourdomain.com`) to `<TUNNEL_ID>.cfargotunnel.com`.
            ```bash
            cloudflared tunnel route dns my-youtube-api-tunnel api.yourdomain.com
            ```

        c.  **Run the tunnel:**
            Make sure your Gunicorn server is running (e.g., `gunicorn app:app --bind 127.0.0.1:8000`).
            Then, run the tunnel, pointing it to your local service:
            ```bash
            cloudflared tunnel run --url localhost:8000 my-youtube-api-tunnel
            ```
            If you didn't configure a custom domain and just want a named `trycloudflare.com` subdomain, you can often just run:
            ```bash
            cloudflared tunnel --name my-youtube-api-tunnel --url localhost:8000
            ```
            (The exact commands and options might vary slightly with `cloudflared` versions, always refer to their official documentation.)

Now your API should be accessible via the Cloudflare tunnel URL.

## API Endpoints

The primary endpoint is `/watch`. Detailed information about its parameters and behavior is available on the landing page (`/`).

## Error Handling

The API returns standard HTTP error codes:
-   `400 Bad Request`: Missing or invalid parameters.
-   `404 Not Found`: Resource not found (e.g., downloaded file not available).
-   `500 Internal Server Error`: Server-side errors during processing.

Error responses are in JSON format with a `description` field.
