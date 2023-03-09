import pyaudio
import wave
from googletrans import Translator

translator = Translator()

import keyboard
from voicevox import Client
import asyncio
from pynput.keyboard import Key, Controller, Listener
keyboard1 = Controller()

import time
from pygame import mixer, _sdl2 as devicer



while True:
    if keyboard.read_key() == "B":
        
        filename = "recorded.wav"
        chunk = 1024
        FORMAT = pyaudio.paInt16
        channels = 1
        sample_rate = 44100
        record_seconds = 5
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,      
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
        frames = []
        print("Recording...")
        for i in range(int(sample_rate / chunk * record_seconds)):      
            data = stream.read(chunk)
            # if you want to hear your voice while recording
            # stream.write(data)
            frames.append(data)
        print("Finished recording.")
        # stop and close stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(filename, "wb")
        # set the channels
        wf.setnchannels(channels)
        # set the sample format
        wf.setsampwidth(p.get_sample_size(FORMAT))
        # set the sample rate
        wf.setframerate(sample_rate)
        # write the frames as bytes
        wf.writeframes(b"".join(frames))
        # close the file
        wf.close()
        import speech_recognition as sr
        r = sr.Recognizer()
        message = ""
        with sr.AudioFile('recorded.wav') as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text)
                translated_text = translator.translate(text, dest='ja')
                message = translated_text.text


            except:
                 print('Sorry.. run again...')


        async def main():
            async with Client() as client:
                audio_query = await client.create_audio_query(
                    message, speaker=1
                )
                with open("play.wav", "wb") as f:
                    f.write(await audio_query.synthesis())


        if __name__ == "__main__":
            asyncio.run(main())
        mixer.init() # Initialize the mixer, this will allow the next command to work
        mixer.init(devicename = devicer.audio.get_audio_device_names(False)[0]) # Initialize it with the correct device
        f=open('play.wav')
        mixer.music.load(f) # Load the mp3
        mixer.music.play() # Play it
        keyboard1.press('i')

        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        keyboard1.release('i')
        f.close()
        time.sleep(1)       
