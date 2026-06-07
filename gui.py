import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import os
import subprocess
import threading
from datetime import datetime
from tkinter.scrolledtext import ScrolledText


class YouTubeDownloaderGUI:
    def __init__(self, root):
        """Initialize the main application window and set up all GUI elements."""
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x760")
        self.root.resizable(True, True)

        # Configure grid weight to make the GUI expandable
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)

        # Initialize variables used by the UI before widgets are created
        self.downloading = False
        self.selected_quality = None
        self.available_qualities = []
        self.subtitle_tracks = {}
        self.no_subtitle_option = "No subtitles"

        # Create and set up all GUI elements
        self.setup_gui_elements()

    def setup_gui_elements(self):
        """Create and arrange all GUI elements in the window."""
        # URL Entry section
        url_frame = ttk.LabelFrame(self.root, text="Video URL", padding=(10, 5))
        url_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.fetch_btn = ttk.Button(url_frame, text="Fetch Video Info", command=self.fetch_video_info)
        self.fetch_btn.grid(row=0, column=1, padx=5, pady=5)

        # Video Information section
        info_frame = ttk.LabelFrame(self.root, text="Video Information", padding=(10, 5))
        info_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ttk.Label(info_frame, text="Title: ")
        self.title_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.duration_label = ttk.Label(info_frame, text="Duration: ")
        self.duration_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # Quality Selection section
        quality_frame = ttk.LabelFrame(self.root, text="Quality Selection", padding=(10, 5))
        quality_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        quality_frame.grid_columnconfigure(0, weight=1)

        self.quality_combobox = ttk.Combobox(quality_frame, state="readonly")
        self.quality_combobox.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Subtitle Selection section
        subtitle_frame = ttk.LabelFrame(self.root, text="Subtitle Selection", padding=(10, 5))
        subtitle_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        subtitle_frame.grid_columnconfigure(0, weight=1)

        self.subtitle_combobox = ttk.Combobox(subtitle_frame, state="readonly")
        self.subtitle_combobox.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.subtitle_combobox["values"] = [self.no_subtitle_option]
        self.subtitle_combobox.set(self.no_subtitle_option)

        # Download section
        download_frame = ttk.LabelFrame(self.root, text="Download Progress", padding=(10, 5))
        download_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        download_frame.grid_columnconfigure(0, weight=1)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(download_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.status_label = ttk.Label(download_frame, text="")
        self.status_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.download_btn = ttk.Button(download_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=2, column=0, padx=5, pady=5)

        # Log section
        log_frame = ttk.LabelFrame(self.root, text="Download Log", padding=(10, 5))
        log_frame.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

        self.log_text = ScrolledText(log_frame, height=10, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def log_message(self, message):
        """Add a message to the log text area."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def check_ffmpeg(self):
        """Check if FFmpeg is installed and accessible."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True)
            return True
        except FileNotFoundError:
            return False

    def get_best_format(self, target_height, ffmpeg_available):
        """Select the best format based on FFmpeg availability."""
        if ffmpeg_available:
            return f'bestvideo[height<={target_height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={target_height}][ext=mp4]/best'
        return f'best[height<={target_height}][ext=mp4]/best[ext=mp4]/best'

    def format_size(self, bytes):
        """Convert bytes to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} GB"

    def progress_hook(self, d):
        """Handle download progress updates."""
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)

            if total:
                percentage = (downloaded / total) * 100
                speed = d.get('speed', 0)
                speed_str = self.format_size(speed) + '/s' if speed else 'N/A'

                eta = d.get('eta', None)
                eta_str = str(datetime.fromtimestamp(eta).strftime('%M:%S')) if eta else 'N/A'

                # Update GUI elements
                self.root.after(0, self.update_progress, percentage, speed_str, eta_str)

    def update_progress(self, percentage, speed, eta):
        """Update progress bar and status label."""
        self.progress_var.set(percentage)
        self.status_label.config(text=f"Speed: {speed} | ETA: {eta}")

    def fetch_video_info(self):
        """Fetch video information and update GUI."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL")
            return

        self.quality_combobox.set("")
        self.subtitle_tracks = {}
        self.subtitle_combobox["values"] = [self.no_subtitle_option]
        self.subtitle_combobox.set(self.no_subtitle_option)
        self.log_message("Fetching video information...")
        threading.Thread(target=self._fetch_video_info_thread, args=(url,), daemon=True).start()

    def _fetch_video_info_thread(self, url):
        """Background thread for fetching video information."""
        try:
            ffmpeg_available = self.check_ffmpeg()
            ydl_opts = {'quiet': True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # Update GUI with video information
                self.root.after(0, self._update_video_info, info, ffmpeg_available)

        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
            self.root.after(0, self.log_message, f"Error: {str(e)}")

    def _update_video_info(self, info, ffmpeg_available):
        """Update GUI with fetched video information."""
        # Update title and duration
        title = info.get('title', 'Unknown')
        duration = int(info.get('duration', 0))
        duration_str = f"{duration // 60}:{duration % 60:02d}"

        self.title_label.config(text=f"Title: {title}")
        self.duration_label.config(text=f"Duration: {duration_str}")

        # Update available qualities
        formats = info.get('formats', [])
        quality_set = set()

        for f in formats:
            height = f.get('height')
            if height and (ffmpeg_available or f.get('acodec') != 'none'):
                quality_set.add(f"{height}p")

        self.available_qualities = sorted(quality_set, key=lambda x: int(x.replace('p', '')))
        self.quality_combobox['values'] = self.available_qualities

        if self.available_qualities:
            self.quality_combobox.set(self.available_qualities[0])

        self.subtitle_tracks = self.get_subtitle_tracks(info)
        subtitle_options = [self.no_subtitle_option, *self.subtitle_tracks.keys()]
        self.subtitle_combobox["values"] = subtitle_options
        self.subtitle_combobox.set(self.no_subtitle_option)

        if self.subtitle_tracks:
            self.log_message(f"Found {len(self.subtitle_tracks)} subtitle track(s)")
        else:
            self.log_message("No subtitle tracks were found for this video")
        self.log_message(f"Video information fetched successfully")

    def get_subtitle_tracks(self, info):
        """Build a label-to-track mapping for manual and auto-generated subtitles."""
        subtitle_tracks = {}

        for source_key, source_label in (("subtitles", "Manual"), ("automatic_captions", "Auto-generated")):
            tracks = info.get(source_key) or {}
            for language_code, formats in sorted(tracks.items()):
                if not formats or language_code == "live_chat":
                    continue

                track_name = next((item.get("name") for item in formats if item.get("name")), language_code)
                label = f"{track_name} ({language_code}) [{source_label}]"
                subtitle_tracks[label] = {
                    "language_code": language_code,
                    "is_auto_generated": source_key == "automatic_captions",
                }

        return subtitle_tracks

    def start_download(self):
        """Start the download process."""
        if self.downloading:
            return

        url = self.url_entry.get().strip()
        quality = self.quality_combobox.get()
        subtitle_label = self.subtitle_combobox.get() or self.no_subtitle_option

        if not url or not quality:
            messagebox.showerror("Error", "Please enter URL and select quality")
            return

        self.downloading = True
        self.download_btn.config(state="disabled")
        self.progress_var.set(0)
        if subtitle_label != self.no_subtitle_option:
            self.log_message(f"Starting download in {quality} with subtitles: {subtitle_label}...")
        else:
            self.log_message(f"Starting download in {quality}...")

        threading.Thread(target=self._download_thread, args=(url, quality, subtitle_label), daemon=True).start()

    def _download_thread(self, url, quality, subtitle_label):
        """Background thread for downloading the video."""
        try:
            height = int(quality.replace('p', ''))
            output_path = 'downloads'
            ffmpeg_available = self.check_ffmpeg()

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            ydl_opts = {
                'format': self.get_best_format(height, ffmpeg_available),
                'progress_hooks': [self.progress_hook],
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')
            }

            selected_subtitle = self.subtitle_tracks.get(subtitle_label)
            if selected_subtitle:
                ydl_opts['subtitleslangs'] = [selected_subtitle['language_code']]
                ydl_opts['subtitlesformat'] = 'srt/best'
                ydl_opts['embedsubtitles'] = ffmpeg_available

                if selected_subtitle['is_auto_generated']:
                    ydl_opts['writeautomaticsub'] = True
                else:
                    ydl_opts['writesubtitles'] = True

                if ffmpeg_available:
                    self.root.after(0, self.log_message, "Selected subtitle will be downloaded and embedded into the video")
                else:
                    self.root.after(
                        0,
                        self.log_message,
                        "FFmpeg was not found. The subtitle will be downloaded as a separate file instead of being embedded."
                    )

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.after(0, self._download_complete)

        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
            self.root.after(0, self.log_message, f"Error: {str(e)}")
            self.root.after(0, self._reset_download_state)

    def _download_complete(self):
        """Handle download completion."""
        self.log_message("Download completed successfully!")
        messagebox.showinfo("Success", "Download completed successfully!")
        self._reset_download_state()

    def _reset_download_state(self):
        """Reset the download state and enable the download button."""
        self.downloading = False
        self.download_btn.config(state="normal")
        self.status_label.config(text="")


def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
