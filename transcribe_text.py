import whisper
import os
import subprocess
import logging
import opencc  # 新增

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract audio from video file using ffmpeg
def extract_audio_from_video(video_file):
    audio_file = os.path.splitext(video_file)[0] + ".mp3"
    command = [
        'ffmpeg',
        '-i', video_file,
        '-q:a', '0',
        '-map', 'a',
        audio_file
    ]
    subprocess.run(command, check=True)
    logging.info(f'Audio extracted to: {audio_file}')
    return audio_file

# Main function to handle the process
def main():
    # Get the video file name from user input
    video_file = input("Please enter the video file name (including extension): ")
    
    # Extract audio from the video file
    audio_file = extract_audio_from_video(video_file)
    
    # Define the output file name
    output_file = os.path.splitext(audio_file)[0] + ".txt"

    # Load the Whisper model
    logging.info('Loading Whisper model...')
    model = whisper.load_model("base")
    logging.info('Whisper model loaded.')

    # Start transcribing with verbose=True to display intermediate status
    logging.info(f'Transcribing the file {audio_file}, please wait...')
    result = model.transcribe(audio_file, verbose=True)
    
    # Extract the transcribed text from the result
    transcribed_text = result['text']

    # Convert Traditional Chinese to Simplified Chinese
    converter = opencc.OpenCC('t2s')  # t2s 表示繁体转简体
    simplified_text = converter.convert(transcribed_text)

    # Write the simplified transcription result to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(simplified_text)

    logging.info(f'Transcription completed! The result has been saved to: {output_file}')

if __name__ == "__main__":
    main()