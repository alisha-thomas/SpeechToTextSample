import os

def gather_audio_files_and_transcripts(base_path):
    audio_files = []
    transcriptions = []
    
    for root, dirs, files in os.walk(base_path):
        # Skip the 'cleaned_audios_zip\31' folder - keeping it for testing model
        # if 'cleaned_audios_zip\\31\\121972' in root:
        #     continue
        
        for file in files:
            if file.endswith(".flac"):
                wav_file_path = os.path.join(root, file)
                path_to_audio = os.path.join(os.getcwd(), wav_file_path)
                audio_files.append(path_to_audio)
                
                # Correcting the path for the corresponding transcription file
                parent_dir = os.path.basename(root)
                grandparent_dir = os.path.basename(os.path.dirname(root))
                transcript_file_name = f"{grandparent_dir}-{parent_dir}.trans.txt"
                transcript_file_path = os.path.join(root, transcript_file_name)
                
                # Reading the transcription file
                if os.path.exists(transcript_file_path):
                    with open(transcript_file_path, 'r') as f:
                        for line in f:
                            parts = line.strip().split(' ', 1)
                            if parts[0] == os.path.splitext(file)[0]:  # Remove .wav extension
                                transcriptions.append(parts[1])
                                break

    return audio_files, transcriptions

def save_lists_to_files(audio_files, transcriptions, audio_file_path='audio_files.txt', transcript_file_path='transcriptions.txt'):
    with open(audio_file_path, 'w') as af:
        for audio in audio_files:
            af.write(audio + '\n')

    with open(transcript_file_path, 'w') as tf:
        for transcript in transcriptions:
            tf.write(transcript + '\n')

def load_lists_from_files(audio_file_path='audio_files.txt', transcript_file_path='transcriptions.txt'):
    with open(audio_file_path, 'r') as af:
        audio_files = [line.strip() for line in af]

    with open(transcript_file_path, 'r') as tf:
        transcriptions = [line.strip() for line in tf]

    return audio_files, transcriptions

# Set the base path to your 'cleaned_audios_zip' directory
base_path = 'train-clean-100'

# Gather the audio files and their transcriptions
audio_files, transcriptions = gather_audio_files_and_transcripts(base_path)

# Save the lists to text files
save_lists_to_files(audio_files, transcriptions)

# Load the lists back from text files
loaded_audio_files, loaded_transcriptions = load_lists_from_files()

# Verify the lists are loaded correctly
print(loaded_audio_files[:5])  # Print first 5 audio file paths
print(loaded_transcriptions[:5])  # Print first 5 transcriptions
