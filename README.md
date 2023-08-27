# Transcribe YouTube

Get a text transcript of a YouTube video via the CLI

# Requirements
Have `OPENAI_API_KEY` in your shell, or have a `.env` file (gitignored!) with your `OPENAI_API_KEY` in the root dir
```
OPENAI_API_KEY=sk-YourAPIKeyGoesHere
```

You must also have [`ffmpeg`](https://ffmpeg.org/download.html) installed and in your `$PATH` (check with `which ffmpeg`)

# Dependencies

Activate a venv called `venv` in the root dir:
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

To add a new dependency:
```
pip install foobar
pip freeze > requirements.txt
```

# Useage

```
python3 transcribe.py https://www.youtube.com/watch?v=pdPYJKqfiqc
```

Or you can pass just the video id
```
python3 transcribe.py pdPYJKqfiqc
```

This will output the following:
```
python3 transcribe.py https://www.youtube.com/watch\?v\=pdPYJKqfiqc
Starting video download.
Downloading Dr Stephen Wolfram says THIS about ChatGPT, Natural Language and Physics
Download completed!
Starting audio extraction.
Audio extraction completed.
Starting audio transcription.
Audio transcription completed at path /Users/myusername/Code/transcribe_youtube/media/pdPYJKqfiqc.txt
FINAL TRANSCRIPT STARTING HERE

If you look at the history of physics, physics has been a fantastic export field that's populated molecular biology, it's populated quantitative finance, it's populated lots of kinds of things. ... we have a better chance to be able to resolve those kinds of things.
```

This will put the video in `./media/{video_id}.mp4`, the audio in `./media/{video_id}.mp3`, and the transcript in `./media/{video_id}.txt`. The `./media` dir is gitignored, but the script does not clean up the video and audio artifacts, so just be aware that it's taking up disk space

# Implementation Details
Uses [`pytube`](https://github.com/pytube/pytube) to install the YouTube video
Uses [`ffmpeg`](https://ffmpeg.org) to extract the audio
Uses [`whisper`](https://github.com/openai/whisper) API to extract the transcript

# Feature Requests
- Accept multiple video ids at once, and process them all in parallel.

- OpenAI's Whisper API has a limit of 25MB, which, if hit, means we break up into 10 minute audio chunks, then concat the transcripts. Feature requests here:
  - Do this in a way that guarantees we don't step over a word-boundary on the cut
  - Do each of the chunks in parallel (would speed up the transcription step for longer videos by a lot)

- Additional CLI flags to perform various operations on the transcript using GPT:
  - Summarize the key points in the video
  - Translate the transcript into different languages
  - Extract keywords or topics discussed in the video
  - Create a list of action items or takeaways from the video
