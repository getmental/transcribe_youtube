import argparse
from openai import OpenAI

client = OpenAI()

def transcribe_audio(file_path):
    file = open(file_path, "rb")
    transcription_response = client.audio.transcribe("whisper-1", file)
    return transcription_response.text

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using OpenAI Whisper")
    parser.add_argument('--path', type=str, required=True, help='Path to the audio file')

    args = parser.parse_args()
    transcription = transcribe_audio(args.path)

    print(transcription)

if __name__ == "__main__":
    main()
