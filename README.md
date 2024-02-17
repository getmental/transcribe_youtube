# Transcribe YouTube

Get a text transcript of a YouTube video via the CLI, then ask an arbitrary question about the transcript to GPT4

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

## Asking a question about the transcript

Pass a second argument in quotes, and the output will finish by answering your question, using the transcript in the context to GPT4.

```
python3 transcribe.py pdPYJKqfiqc "Briefly summarize the top three key insights from the video"
```

This will output GPT4's answer to your question, at the end of the output logs from the script.

```
Starting video download.
Downloading Dr Stephen Wolfram says THIS about ChatGPT, Natural Language and Physics
Download completed!
Starting audio extraction.
Audio extraction completed.
Starting audio transcription.
Audio transcription completed at path /Users/tsheaff/Code/getmental/transcribe_youtube/media/pdPYJKqfiqc.txt
FINAL TRANSCRIPT STARTING HERE

If you look at the history of physics, physics has been a fantastic export field that's populated molecular biology, it's populated quantitative finance, it's populated lots of kinds of things. ... we have a better chance to be able to resolve those kinds of things.


QUESTION:  Briefly summarize the top three key insights from the video
GPT4's ANSWER:
1. **Interplay Between Physics and LLMs**: Dr. Stephen Wolfram highlights the potential for physics to significantly contribute to understanding and advancing language models, particularly large language models (LLMs) like ChatGPT. He suggests that the methodology and analytical tools developed in physics can help decipher the operational mechanics of LLMs, offering insights into why and how they can produce meaningful, coherent text despite the absence of explicit instructions or examples for every possible query. This could lead to a deeper understanding of the principles underpinning LLM functionality.

2. **LLMs, Language, and Logic**: Wolfram points out that LLMs have an inherent ability to grasp and generate not just syntactically correct sentences but also logically coherent text based on the context provided, akin to human logical reasoning. He draws a parallel between LLMs’ ability to 'discover logic' in constructing language and how Aristotle identified logical structures in rhetoric. This capability surpasses mere syntax adherence, indicating that LLMs can infer some level of semantic grammar or common sense reasoning that guides their text generation.

3. **Workflow Enhancement with LLMs**: Wolfram outlines a practical workflow where LLMs can bridge the gap between natural language input and computational language output. This process entails a user starting with a vague idea, articulating it in natural language, and using an LLM to generate a computational representation in a language like Wolfram Language. This representation can then be refined for accuracy, serving as a basis for further computational work. Wolfram emphasizes this as a significant advancement in making computational tasks more accessible and intuitive for users, while also noting the potential for LLMs in education and solving complex problems like physics word problems through improved understanding of natural language descriptions.
```

### Examples of things you could ask
- Summarize the key points in the video
- Translate the transcript into different languages
- Extract keywords or topics discussed in the video
- Create a list of action items or takeaways from the video


# Implementation Details
Uses [`pytube`](https://github.com/pytube/pytube) to install the YouTube video.

Uses [`ffmpeg`](https://ffmpeg.org) to extract the audio.

Uses [`whisper`](https://github.com/openai/whisper) API to extract the transcript.

# Feature Requests
- Accept multiple video ids at once, and process them all in parallel.

- OpenAI's Whisper API has a limit of 25MB, which, if hit, means we break up into 10 minute audio chunks, then concat the transcripts. Feature requests here:
  - Do this in a way that guarantees we don't step over a word-boundary on the cut
  - Do each of the chunks in parallel (would speed up the transcription step for longer videos by a lot)
