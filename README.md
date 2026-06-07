# YTDownloader

YTDownloader is a small Python project for downloading individual YouTube videos with `yt-dlp`.

The project currently exposes two ways to use it:

- `gui.py`: a desktop GUI built with `tkinter`
- `cli.py`: an interactive terminal workflow

This README describes the code as it exists now, including what is supported, what is not, and the practical differences between the GUI and CLI.

## Current Support Summary

| Capability | GUI | CLI | Notes |
| --- | --- | --- | --- |
| Single video download | Yes | Yes | This is the main supported workflow. |
| Playlist download | No | No | There is no dedicated playlist handling in either interface. |
| Bulk or multi-URL download | No | No | Both interfaces accept one URL at a time. |
| Quality selection | Yes | Yes | Based on formats returned by `yt-dlp`. |
| Download progress display | Yes | Yes | GUI shows a progress bar and log; CLI prints inline progress. |
| Custom output directory | No | No | Output is hardcoded to `downloads/`. |
| Audio-only download | No | No | The current project is video-focused only. |
| Members-only or login-required videos | Yes, with browser cookies | No | The GUI can load cookies from a supported local browser session. |
| Subtitle or CC download | Yes | No | The GUI can download one selected subtitle track for the current video. |
| Subtitle embedding into video | Yes, with FFmpeg | No | The GUI embeds the selected subtitle when FFmpeg is available; otherwise it saves a separate subtitle file. |
| Works without FFmpeg | Yes, with limits | Yes, with limits | Both interfaces fall back to compatible video formats; subtitle embedding still needs FFmpeg. |

## Project Files

- `gui.py`: launches the desktop interface
- `cli.py`: launches the terminal-based interactive downloader
- `requirements.txt`: project dependency list
- `main.py`: currently empty and not used as an entry point

If you want to run the project, use `gui.py` or `cli.py`. Do not use `main.py`.

## Requirements

You need:

- Python 3
- `pip`
- `yt-dlp` from `requirements.txt`
- `tkinter` if you want the GUI
- FFmpeg if you want the best compatibility and higher-quality downloads

### About `tkinter`

The GUI imports `tkinter` from the Python standard library, but on some Linux distributions you may still need to install the OS package separately.

Quick check:

```bash
python -c "import tkinter; print('tkinter is available')"
```

If that fails on Debian or Ubuntu, the package is often:

```bash
sudo apt install python3-tk
```

### About FFmpeg

FFmpeg is important for this project because many higher-quality downloads are delivered as separate video and audio streams that need to be merged.

Quick check:

```bash
ffmpeg -version
```

If that command fails, install FFmpeg and make sure it is on your system `PATH`.

Common examples:

```bash
# Ubuntu / Debian
sudo apt install ffmpeg

# macOS with Homebrew
brew install ffmpeg

# Windows with Chocolatey
choco install ffmpeg
```

The exact install command may vary by platform and package manager.

## Setup

From the project root:

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

After installation, you can use either the GUI or the CLI.

## Where Downloads Are Saved

Both interfaces save files to a folder named `downloads/` using this naming template:

```text
%(title)s.%(ext)s
```

Important detail:

- If you launch the script from the project root, files will go to `./downloads`
- If you launch the script from another directory, the `downloads/` folder will be created relative to that working directory

If you want the output folder to stay inside this repository, run the commands from the project root.

## Using the GUI

### Start the GUI

Run:

```bash
python gui.py
```

This opens a desktop window titled `YouTube Video Downloader`.

### Browser Session Support

The GUI now includes a `Browser Session` section above the video information panel.

You can use it when:

- a YouTube video is members-only
- a video is age-restricted
- YouTube asks you to sign in
- YouTube triggers the `confirm you're not a bot` check and your browser session already has access

Supported browser names currently exposed by the GUI:

- `brave`
- `chrome`
- `chromium`
- `edge`
- `firefox`
- `opera`
- `safari`
- `vivaldi`
- `whale`

There is also an optional `Profile / path` field for cases where:

- your browser uses a non-default profile
- your browser data lives in a custom path
- you need to point `yt-dlp` at a specific local browser profile

For more advanced browser-cookie setups, the GUI also exposes:

- `Chromium keyring (optional)` for Chromium-based browsers on Linux
- `Firefox container (optional)` for Firefox Multi-Account Containers

Supported keyring values currently exposed by the GUI:

- `BASICTEXT`
- `GNOMEKEYRING`
- `KWALLET`
- `KWALLET5`
- `KWALLET6`

Firefox container behavior:

- leave it blank to load cookies from all containers
- enter a container name to load only that Firefox container
- enter `none` to load only cookies that do not belong to any Firefox container

If you do not need authenticated access, leave the browser selection on `No browser cookies`.

### GUI Workflow

1. Paste a single YouTube video URL into the `Video URL` field.
2. If the video requires login, select your browser in the `Browser Session` section.
3. Optionally fill `Profile / path` if you are not using the browser's default profile.
4. Optionally choose a Chromium keyring override if your browser cookies are encrypted with a non-default Linux keyring backend.
5. Optionally fill `Firefox container` if you need cookies from one Firefox container only.
6. Click `Fetch Video Info`.
7. Wait for the app to fetch metadata.
8. Confirm that the video title and duration appear in the `Video Information` section.
9. Choose a quality from the dropdown.
10. Optionally choose a subtitle track from the subtitle dropdown.
11. Click `Download`.
12. Watch the progress bar, speed/ETA label, and log area while the download runs.
13. When the download finishes, the app shows a success dialog and the file is saved into `downloads/`.

### Important GUI Behavior

- The GUI is built for one URL at a time.
- It allows only one active download at a time.
- The quality dropdown is sorted from lowest resolution to highest resolution.
- The GUI automatically selects the first available quality after fetching metadata.
- The subtitle dropdown always includes a `No subtitles` option.
- If subtitle tracks are available, the dropdown can include both creator-provided subtitles and auto-generated captions.
- Subtitle labels include whether the track is `Manual` or `Auto-generated`.
- The browser selection is used for both metadata fetch and the actual download, so members-only access is handled consistently across both steps.
- The keyring override is only relevant for Chromium-based browsers on Linux.
- The Firefox container field is only relevant when `firefox` is selected as the browser source.

That last point matters: if you want a higher resolution, change the dropdown before clicking `Download`.

### What the GUI Does Not Currently Offer

- No playlist mode
- No multi-URL queue
- No bulk downloader
- No audio-only mode
- No folder picker for choosing a different output location
- No pause, cancel, or resume controls
- No command-line arguments for automation
- No subtitle search or filtering beyond the dropdown list
- No subtitle support in the CLI yet

### GUI and FFmpeg

The GUI checks for FFmpeg both when it builds the quality list and when it starts the download.

Practical takeaway:

- With FFmpeg installed, the GUI can use separate video/audio streams and embed a selected subtitle track into the video
- Without FFmpeg, the GUI falls back to merged video formats when possible
- Without FFmpeg, a selected subtitle track is downloaded as a separate subtitle file instead of being embedded into the video

If you want the smoothest experience in the GUI, install FFmpeg first.

### GUI and Browser Cookies

The GUI passes browser cookies directly to `yt-dlp` when you select a browser session.

Practical takeaway:

- use browser cookies for members-only or login-required videos
- make sure that selected browser profile is already logged into YouTube
- if cookie extraction fails, check whether you need a different profile path or whether your browser stores cookies in a custom location
- for Chromium on Linux, try a different keyring value if cookie decryption fails
- for Firefox, use a container name or `none` when the needed session lives inside one container only

## Using the CLI

### Start the CLI

Run:

```bash
python cli.py
```

### What Kind of CLI This Is

This is not a flag-driven command-line tool.

In other words:

- It does not currently support options like `--url`, `--quality`, `--playlist`, or `--output`
- It prompts you interactively with `input()` calls in the terminal

So the CLI is best understood as a terminal wizard, not as a fully scriptable automation interface.

### CLI Workflow

1. Run `python cli.py`.
2. Paste a single video URL when prompted.
3. Either:
   - type an exact quality like `720p`, or
   - press Enter to see the available qualities first
4. The script fetches video metadata.
5. It prints the video title and duration.
6. It prints the available resolutions as a numbered list.
7. If you did not enter a valid quality up front, it asks you to choose one by number.
8. It downloads the video into `downloads/`.
9. It prints progress updates in the terminal, including percentage, speed, and ETA.

### Example CLI Session

```text
$ python cli.py
Enter YouTube video URL: https://www.youtube.com/watch?v=EXAMPLE
Enter preferred quality (e.g., 720p) or press Enter to see available options:

Fetching video information...

Video Title: Example Video
Duration: 8:31

Available qualities:
1. 360p
2. 720p
3. 1080p

Please select a quality from the available options:
Enter the number of your choice: 2

Downloading video in 720p...
Progress: 42.1% | Speed: 3.50 MB/s | ETA: 00:18
```

### CLI Quality Selection Rules

The CLI behaves like this:

- If you type a quality string that exists in the discovered quality list, the script uses it
- If you leave the quality blank, it shows the numbered list and asks you to choose
- If you type a quality that is not available, it also falls back to the numbered selection flow

### CLI and FFmpeg

The CLI has explicit fallback logic for systems where FFmpeg is not installed.

With FFmpeg installed:

- the script can request separate best video and best audio streams
- this usually gives you better quality choices

Without FFmpeg:

- the script warns you that quality options may be limited
- it only lists formats that already contain audio
- high resolutions may disappear from the available quality list

So the CLI can still work without FFmpeg, but you should expect fewer format choices.

## Subtitles and Closed Captions

The current subtitle support is split by interface:

- GUI: can optionally download one subtitle track for the selected video
- CLI: does not currently download subtitles or closed captions

### What the GUI Can Do

If the fetched video exposes subtitle tracks through `yt-dlp`, the GUI can:

- show a subtitle dropdown after you click `Fetch Video Info`
- list manual and auto-generated tracks separately
- download the selected track together with the video
- embed the selected track into the video when FFmpeg is installed
- save the selected track as a separate subtitle file when FFmpeg is not installed
- reuse the same selected browser session for subtitle-capable downloads that require YouTube authentication

### What the CLI Still Cannot Do

The current CLI code still does not request subtitles at all.

That means:

- if a YouTube video has creator-uploaded English subtitles, the CLI does not fetch them
- if a YouTube video has auto-generated English captions, the CLI does not fetch them either
- the CLI-downloaded video file will not include subtitle tracks added by YouTube unless you use plain `yt-dlp` directly outside this app

### Important Distinction: Hardcoded vs Separate Subtitles

There are two very different cases:

1. Hardcoded or burned-in subtitles:
   If the subtitle text is already drawn into the video image itself, it will remain in the downloaded video because it is part of the picture.
2. YouTube subtitle tracks or CC:
   These are separate text tracks hosted by YouTube. They are only included when the downloader explicitly requests them. In this project, that support currently exists in the GUI only.

Example scenario:

- Chinese video
- uploader added English CC on YouTube

With the current GUI:

- if that English CC appears in the subtitle dropdown and you select it, the GUI will download it
- if FFmpeg is available, the GUI will ask `yt-dlp` to embed it into the downloaded video
- if FFmpeg is not available, the GUI will keep it as a separate subtitle file alongside the video

### Why the CLI Still Does Not Include Subtitles

Only the GUI currently configures subtitle-related `yt-dlp` options.

The CLI still does not set subtitle-related options such as:

- writing subtitle files
- downloading auto-generated subtitles
- embedding subtitle tracks into the final media file

If you want subtitle automation in the terminal today, use plain `yt-dlp` directly.

## How to Download Subtitles with `yt-dlp`

### First: Inspect What Subtitle Tracks Exist

Run:

```bash
yt-dlp --list-subs "VIDEO_URL"
```

This is the first command you should use when the video may have:

- multiple languages
- manual subtitles and auto-generated subtitles
- multiple English variants

### Download Creator-Provided Subtitles Only

If you want the creator's uploaded English subtitles only:

```bash
yt-dlp --write-subs --sub-langs en --skip-download "VIDEO_URL"
```

Notes:

- `--write-subs` is for normal subtitle files
- `--skip-download` tells `yt-dlp` to download only the subtitle track, not the video

### Download Auto-Generated English Captions Only

If the English caption is auto-generated by YouTube:

```bash
yt-dlp --write-auto-subs --sub-langs en --skip-download "VIDEO_URL"
```

Notes:

- `--write-auto-subs` is separate from `--write-subs`
- auto-generated captions are not the same thing as creator-uploaded subtitle files

### Download the Video and the Creator-Provided English Subtitle Together

```bash
yt-dlp -f "bestvideo+bestaudio/best" --write-subs --sub-langs en "VIDEO_URL"
```

This will usually give you:

- a video file
- a separate subtitle file such as `.vtt` or `.srt`, depending on what is available and what you request

### Prefer `srt` When You Want Broad Player Compatibility

```bash
yt-dlp -f "bestvideo+bestaudio/best" --write-subs --sub-langs en --sub-format "srt/best" "VIDEO_URL"
```

If `srt` is not available, `yt-dlp` will fall back according to the preference order you provide.

## How to Embed Subtitles into the Video

The easiest method is to let `yt-dlp` do it during download.

### Embed Creator-Provided English Subtitles

```bash
yt-dlp -f "bestvideo+bestaudio/best" --write-subs --sub-langs en --embed-subs "VIDEO_URL"
```

### Embed Auto-Generated English Captions

```bash
yt-dlp -f "bestvideo+bestaudio/best" --write-auto-subs --sub-langs en --embed-subs "VIDEO_URL"
```

### Embed While Preferring a Specific Subtitle Format

```bash
yt-dlp -f "bestvideo+bestaudio/best" --write-subs --sub-langs en --sub-format "srt/best" --embed-subs "VIDEO_URL"
```

Practical notes:

- embedding subtitles requires FFmpeg
- embedding is cleaner when you do it in the same `yt-dlp` command rather than as a separate later step
- many players also work fine with an external subtitle file, so embedding is optional

## How to Choose the Right English Track

Use:

```bash
yt-dlp --list-subs "VIDEO_URL"
```

Then decide based on what is listed.

### If You Want the Creator's Uploaded English CC

Use only:

```bash
--write-subs --sub-langs en
```

This targets the normal subtitle track, not the auto-generated one.

### If You Want the Auto-Generated English CC

Use only:

```bash
--write-auto-subs --sub-langs en
```

This targets YouTube's automatic caption track.

### If the Video Has Multiple English Variants

Examples might include:

- `en`
- `en-US`
- `en-GB`
- other English-related tags shown by `--list-subs`

In that case, you can target a broader pattern:

```bash
yt-dlp --write-subs --sub-langs "en.*" --skip-download "VIDEO_URL"
```

That tells `yt-dlp` to match English subtitle language tags using a regex-style pattern.

### Manual vs Auto-Generated with the Same Language

If the video offers both:

- creator-uploaded English subtitles
- English auto-generated captions

Do not rely on one combined command if you need precise control over which one you keep.

Use separate runs instead:

```bash
# Manual / creator-provided English subtitles
yt-dlp --write-subs --sub-langs en --skip-download "VIDEO_URL"

# Auto-generated English captions
yt-dlp --write-auto-subs --sub-langs en --skip-download "VIDEO_URL"
```

That avoids ambiguity and makes it obvious which file came from which subtitle source.

## If You Already Downloaded the Video Without Subtitles

You have two options.

### Option 1: Keep Subtitles as a Separate File

This is the simplest approach.

Download the subtitle track only:

```bash
yt-dlp --write-subs --sub-langs en --skip-download "VIDEO_URL"
```

Many video players will automatically detect an external subtitle file if it sits next to the video and has a matching base filename.

### Option 2: Mux the Subtitle into a New Video File with FFmpeg

If you already have:

- a video file
- a subtitle file

you can merge them manually.

For MP4:

```bash
ffmpeg -i input.mp4 -i subtitles.srt -c copy -c:s mov_text output-with-subs.mp4
```

For MKV:

```bash
ffmpeg -i input.mp4 -i subtitles.srt -c copy output-with-subs.mkv
```

Practical recommendation:

- use `mkv` if you want fewer subtitle format restrictions
- use `mp4` only if you specifically need MP4 compatibility

## Recommended Subtitle Workflows

### Best Simple Workflow

If you want English creator-provided subtitles embedded:

```bash
yt-dlp -f "bestvideo+bestaudio/best" --write-subs --sub-langs en --embed-subs "VIDEO_URL"
```

### Best Workflow When You Only Need a Separate Subtitle File

```bash
yt-dlp --write-subs --sub-langs en --skip-download "VIDEO_URL"
```

### Best Workflow When the Video Only Has Auto-Generated English Captions

```bash
yt-dlp -f "bestvideo+bestaudio/best" --write-auto-subs --sub-langs en --embed-subs "VIDEO_URL"
```

### Best Workflow When You Are Unsure What Exists

```bash
yt-dlp --list-subs "VIDEO_URL"
```

Run that first, then choose between `--write-subs` and `--write-auto-subs`.

## Playlist and Bulk Download Status

This project is currently designed around a single video per run.

### Playlist URLs

Playlist downloading is not implemented as a supported workflow in either interface.

Why:

- the GUI has one URL field and one quality dropdown for one item
- the CLI asks for one URL and one quality choice
- both interfaces derive quality options from a single video's `formats` list

Practical conclusion:

- Use single video URLs
- Do not expect playlist URLs to work cleanly
- If you pass a playlist URL, behavior may be incomplete, confusing, or fail during metadata or quality selection

### Bulk or Multi-URL Download

Bulk downloading is also not available right now.

There is:

- no queue input in the GUI
- no paste-many workflow in the GUI
- no loop over multiple URLs in the CLI
- no text-file input mode
- no batch command syntax

If you want multiple videos, you currently need to run one download at a time.

## Troubleshooting

### `ModuleNotFoundError: No module named 'yt_dlp'`

Install dependencies:

```bash
pip install -r requirements.txt
```

### `ffmpeg` is missing

Install FFmpeg and confirm:

```bash
ffmpeg -version
```

This is especially important for the GUI and for higher-quality downloads in general.

### The GUI does not start because of `tkinter`

Install the Tk bindings for your Python distribution. On Debian or Ubuntu, this is commonly:

```bash
sudo apt install python3-tk
```

### Members-only, age-restricted, or login-required YouTube videos in the GUI

Use the GUI's `Browser Session` section before you click `Fetch Video Info`.

Recommended order:

1. log into YouTube in your normal browser
2. select that browser in the GUI
3. fill `Profile / path` only if you are not using the default profile
4. if you use Chromium on Linux, set `Chromium keyring` when your cookies are stored in a non-default keyring backend
5. if you use Firefox containers, fill `Firefox container` with the needed container name or `none`
6. fetch video information again

If the GUI still fails:

- confirm that the selected browser profile is the one with your active YouTube membership
- confirm that the browser session can open the same video normally
- if you are on Linux and using a Chromium-based browser, cookie decryption may also depend on the selected keyring backend
- if you are using Firefox containers, confirm that the chosen container name matches the container where your signed-in YouTube session actually lives

### Video information fetch fails or a download errors out

Common causes:

- the URL is invalid
- the video is private, removed, or age-restricted
- your internet connection is unstable
- `yt-dlp` needs to be updated because the target site changed

Update `yt-dlp` with:

```bash
pip install --upgrade yt-dlp
```

### YouTube says `No supported JavaScript runtime could be found`

Recent `yt-dlp` versions rely on an external JavaScript runtime for full YouTube extraction support.

The official `yt-dlp` EJS guide currently says:

- `deno` is the recommended runtime
- `node` is also supported when explicitly enabled with `--js-runtimes node`

Examples:

```bash
# If you have deno installed and on PATH
yt-dlp --list-subs "VIDEO_URL"

# If you have node installed and on PATH
yt-dlp --js-runtimes node --list-subs "VIDEO_URL"
```

If no supported runtime is installed, YouTube extraction may be incomplete and some formats or metadata may be missing.

### YouTube says `Sign in to confirm you're not a bot`

That is a YouTube anti-bot / authentication problem, not a subtitle-option problem.

In practice, the subtitle flags can be correct and the download can still fail before subtitle handling even starts.

The official `yt-dlp` guidance is to use browser cookies when YouTube requires authentication.

Common example:

```bash
yt-dlp --cookies-from-browser firefox --list-subs "VIDEO_URL"
```

Then combine cookies with your actual download command:

```bash
yt-dlp --cookies-from-browser firefox -f "bestvideo+bestaudio/best" --write-subs --sub-langs en --sub-format "srt/best" --embed-subs "VIDEO_URL"
```

If you use Chromium-based browsers on Linux, `yt-dlp` may also need access to the system keyring to decrypt browser cookies correctly.

### Best Order of Operations for Subtitle Downloads on YouTube

If a subtitle-enabled YouTube command fails, debug it in this order:

1. confirm `yt-dlp` is updated
2. confirm a supported JS runtime is installed
3. run `--list-subs` first
4. add `--cookies-from-browser` if YouTube triggers the bot-check
5. only then run the full subtitle download or embed command

### Running `python main.py` does nothing

That is expected with the current repository state. Use:

```bash
python gui.py
```

or:

```bash
python cli.py
```

## Practical Recommendations

If you just want the shortest path to success:

1. Install dependencies from `requirements.txt`
2. Install FFmpeg
3. Run the project from the repository root
4. Use a single YouTube video URL
5. Use `python gui.py` if you want a visual workflow
6. Use `python cli.py` if you prefer the terminal

## Current Limitations Recap

The current codebase does not yet provide:

- true playlist downloading
- bulk download support
- a queue system
- automation-friendly CLI flags
- custom output directory selection
- audio-only downloads

If you keep those boundaries in mind, the current project is straightforward: it is a single-video downloader with both a GUI path and an interactive terminal path.
