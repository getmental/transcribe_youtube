import argparse
from pydub import AudioSegment
from pytube import YouTube
import os
import openai

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# run via `python3 src/playground/notebooks/summarizer/summarizer.py aQfeYBa1MTk`


def download_video(url, filename, dir_path="."):
    print("Starting video download.")
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    print(f"Downloading {yt.title}")
    stream.download(output_path=dir_path, filename=filename)
    print("Download completed!")
    return f"{dir_path}/{filename}"


def extract_audio(video_path, output_audio_path):
    print("Starting audio extraction.")
    cmd = f"ffmpeg -i {video_path} -q:a 0 -map a {output_audio_path} -y -loglevel 0"
    os.system(cmd)
    print("Audio extraction completed.")
    return output_audio_path


def transcribe_audio(audio_path, output_transcription_path):
    print("Starting audio transcription.")

    # check if the audio_path is more than 25MB
    whisper_max_size = 25 * 1024 * 1024
    if os.path.getsize(audio_path) > 0.9 * whisper_max_size:
        print("Audio file is too large for OpenAI API.")
        # if it is, then we need to split it into 10 minute chunks
        audio_segment = AudioSegment.from_mp3(audio_path)
        ten_minutes = 10 * 60 * 1000
        chunks = [
            audio_segment[i : i + ten_minutes]
            for i in range(0, len(audio_segment), ten_minutes)
        ]

        print(f"Broke file into {len(chunks)} chunks")

        # and then transcribe each chunk
        transcriptions = []
        for i, chunk in enumerate(chunks):
            audio_file_name = os.path.splitext(os.path.basename(audio_path))[0]
            chunk_file_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "media",
                f"{audio_file_name}_chunk_{i}.mp3",
            )
            chunk.export(chunk_file_path, format="mp3")
            file = open(chunk_file_path, "rb")
            transcription_response = openai.Audio.transcribe("whisper-1", file)
            transcriptions.append(transcription_response["text"])
            print(f"Finished transcribing chunk {i}")
            file.close()
            os.remove(chunk_file_path)

        # then combine the transcriptions into one file
        transcription = " ".join(transcriptions)
    else:
        file = open(audio_path, "rb")
        transcription_response = openai.Audio.transcribe("whisper-1", file)
        transcription = transcription_response["text"]
        file.close()

    with open(output_transcription_path, "w") as f:
        f.write(transcription)
    print(f"Audio transcription completed at path {output_transcription_path}")
    print("FINAL TRANSCRIPT STARTING HERE\n")
    print(transcription)
    return output_transcription_path


def main():
    parser = argparse.ArgumentParser(description="Process YouTube video id.")
    parser.add_argument("video_id", type=str, help="YouTube video id")
    args = parser.parse_args()

    # if the video_id is the full youtube url, parse out just the video id
    video_id = args.video_id
    if video_id.startswith("https://www.youtube.com/watch?v="):
        video_id = video_id.split("=")[1]

    dir = os.path.dirname(os.path.realpath(__file__)) + "/media"
    video_path = download_video(
        f"https://www.youtube.com/watch?v={video_id}", f"{video_id}.mp4", dir
    )
    audio_path = extract_audio(video_path, f"{dir}/{video_id}.mp3")
    transcribe_audio(audio_path, f"{dir}/{video_id}.txt")


if __name__ == "__main__":
    main()
