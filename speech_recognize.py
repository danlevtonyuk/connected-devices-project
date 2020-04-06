
import speech_recognition as sr
r = sr.Recognizer()

list_text = ['a lumpy','hey Lumpy', 'lamp', 'Halen', 'Hayden', 'listen', 'Listen', 'Lampe', 'lampe']

while(True):
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        print(" - Please speak for 5 seconds...")
        audio_data = r.record(source, duration=5)
        #print(" - Recognizing...")
        # convert speech to text
        #text = r.recognize_google(audio_data)
        try:
            text = r.recognize_google(audio_data, language="en-EN")
            print(text)
            for i in range(0,len(list_text)):
                #print(list_text[i])
                if text in list_text[i]:
                    print("    - LAMPI detected")
                    break
        except:
            print("    - no word recognized!")

