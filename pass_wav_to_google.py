#!/usr/bin/python3
import speech_recognition as sr
import pyaudio


"""cleaned_01.wav",
 "cleaned_01_boost2.wav",
 "cleaned_01_boost4.wav",
 "cleaned_01_boost8.wav",
 "cleaned_01_gain_0.wav",
 "cleaned_01_gain_m3.wav",
 "cleaned_03.wav",
 "cleaned_03_boost2.wav",
 "cleaned_03_boost4.wav",
 "cleaned_03_boost8.wav",
 "cleaned_05.wav",
 "cleaned_05_boost2.wav",
 "cleaned_05_boost4.wav",
 "cleaned_05_boost8.wav",
 "cleaned_09.wav",
 "cleaned_09_boost2.wav",
 "cleaned_09_boost4.wav",
 "cleaned_09_boost8.wav",
 "pre_filtered_02%3A27%3A47.wav",
 "pre_filtered_audio.wav",
 "pre_filtered_audio1587430943.5698678.wav",
 "pre_filtered_audio1587431060.229223.wav",
 "pre_filtered_audio1587431702.2842717.wav",
 "pre_filtered_audio1587431923.0573134.wav",
 """
 
files = [
 "pre_filtered_02%3A00%3A50.wav",
 "pre_filtered_02%3A00%3A50_filter1.wav",
 "pre_filtered_02%3A00%3A50_filter2.wav",
]

r = sr.Recognizer()

for each_file in files:
  eFile = sr.AudioFile(each_file)
  with eFile as source:
    audio = r.record(source)
    print(each_file, type(audio))
    print(r.recognize_google(audio, language="en-EN", show_all=True))
