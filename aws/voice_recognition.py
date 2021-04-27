# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

listOfWords = []
r = sr.Recognizer()
lengthOfEntireClip = 0

def get_large_audio_transcription(path):
    global lengthOfEntireClip 
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path) 
    lengthOfEntireClip = sound.duration_seconds
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
                unhandle = 0 # TODO: unhandled exception
                # print("Error:", str(e))
            else:
                
                text = f"{text.capitalize()}. "
                if("idea" in text):
                    # print("idea was found!!!")
                    timestamps.append([time, audio_chunk.duration_seconds])
                
                # print(chunk_filename, ":", text)
                listOfWords.append(text);

        time += audio_chunk.duration_seconds #increase the timestamp which will be used to decide which clip to select 

                

                # whole_text += text
    # return the text for all chunks detected

    
    return timestamps



timestamps = get_large_audio_transcription("test-3.wav")
print("oldtimestamps", timestamps)
if (timestamps):
    out = []

    prev = 0
    old_time_stamp = [0,0]
    for timestamp in timestamps:
        s =  timestamp[0]
        f =  min(s+20,lengthOfEntireClip) 
        print("s,f", s,f)
        if prev == 0: # first element add to list
            old_time_stamp[0] = s
            old_time_stamp[1] = f
            prev = f
        elif prev != 0 and prev >= s : # if the previous ts has an f that is greater
            old_time_stamp[1] = f
            prev = f
        else:
            #export the old
            out.append(old_time_stamp)
            old_time_stamp = [0,0]
        prev = f
    if old_time_stamp[1]!= 0:
        out.append(old_time_stamp)
    
    print(out)








