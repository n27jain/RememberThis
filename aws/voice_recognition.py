# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

listOfWords = []
r = sr.Recognizer()
def get_large_audio_transcription(path):

    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=True,
    )
    timestamps = []
    time = 0
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=0):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                
                text = f"{text.capitalize()}. "
                if("idea" in text):
                    print("idea was found!!!")
                    timestamps.append(time)
                
                # print(chunk_filename, ":", text)
                listOfWords.append(text);

        time += audio_chunk.duration_seconds #increase the timestamp which will be used to decide which clip to select 

                

                # whole_text += text
    # return the text for all chunks detected

    
    return timestamps




print(get_large_audio_transcription("Eastern Ave.wav"))