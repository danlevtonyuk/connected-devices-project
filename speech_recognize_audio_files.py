#!/usr/bin/python3
import speech_recognition as sr
import colorsys
import pygame, time
from gtts import gTTS 
import os 
import pyaudio
from datetime import datetime
from pocketsphinx import AudioFile, get_model_path, get_data_path


files = os.listdir("AUdioFiles")
files = [x for x in files if x.find("piece") != -1]


def getaudiodevices():
    p = pyaudio.PyAudio()
    print("audio devices", p.get_device_count())
    for i in range(p.get_device_count()):
        name_i = p.get_device_info_by_index(i).get('name')
        print("name_i:", name_i, name_i.find("PnP"))
        print(p.get_device_info_by_index(i).get('name'))
        if name_i.find("PnP") != -1:
          return i
    return None

class LampiSpeech(object):
    def __init__(self):
        self.hue = 1.0
        self.brightness = 1.0
        self.saturation = 1.0
        self.on_off = True
        pyaudio.PyAudio()

    def listenRoutine(self):
        r = sr.Recognizer()

        for each_file in files:
            print(each_file)
            model_path = get_model_path()
            data_path = get_data_path()

            config = {
                'verbose': False,
                'audio_file': os.path.join(os.getcwd(), 'audioFiles', each_file),
                'buffer_size': 2048,
                'no_search': False,
                'full_utt': False,
                'hmm': os.path.join(model_path, 'en-us'),
                'lm': os.path.join(os.getcwd(), "TAR9991/TAR9991/9991.lm"),
                'dict': os.path.join(os.getcwd(), "TAR9991/TAR9991/9991.dic")
            }
            #print (config)

            audio = AudioFile(**config)
            for phrase in audio:
                print(phrase)
            
            with sr.AudioFile(os.path.join(os.getcwd(), "audioFiles", each_file)) as source2:
              recording = r.record(source2)
              print(r.recognize_google(recording, language="en-EN", show_all=True))


        exit()
        if 0:
          eFile = sr.AudioFile(each_file)
          with eFile as source:
            audio = r.record(source)
            print(each_file, type(audio))
            print(r.recognize_google(audio, language="en-EN", show_all=True))
            
            #print(r.recognize_sphinx(audio, grammar="TAR9991/TAR9991/"))
        exit()
        
        print("\r\n\r\n*****\r\nr", r)
        list_text = ['a lumpy','hey Lumpy', 'lamp', 'Halen', 'Hayden', 'listen', 'Listen', 'Lampe', 'lampe']
        stop_flag = True
        duration = 5
        while(stop_flag):
            config = {'color': {'hue':self.hue, 'saturation':self.saturation},
                  'brightness': self.brightness,
                  'on': self.on_off,
                  'client': 'local'}

            print("    - mqtt saved:",config)

            our_device = getaudiodevices()
            print("Detected our mic:", our_device)
            with sr.Microphone(device_index=our_device, sample_rate=48000) as source:
                print("Microphone source:", source, source.__dict__.keys(), source.device_index)
                print(" - Call lampi (",duration, "seconds ) ...")
                print("Set minimum energy threshold to {}".format(r.energy_threshold))
                r.adjust_for_ambient_noise(source)
                audio_data = r.record(source, duration=duration)
                #print(type(audio_data))
                filename = "pre_filtered_" + datetime.now().strftime("%H:%M:%S") + ".wav"
                with open(filename, "wb") as audio_file:
                    audio_file.write(audio_data.get_wav_data())
                exit()
                #print(" - Recognizing...")
                # convert speech to text
                #text = r.recognize_google(audio_data)
                try:
                    text = r.recognize_google(audio_data, language="en-EN")
                    print(" - heard: ",text)
                    text = text.split(" ")
                    for item in text:
                        #print(list_text[i])
                        if item in list_text:
                            print(" - LAMPI detected")
                            
                            pygame.init()
                            pygame.mixer.music.load('this_is_lampi.mp3')
                            pygame.mixer.music.play()
                            time.sleep(3)
                            pygame.mixer.music.fadeout(5)
                            
                            #stop_flag = False
                            self.commandRoutine()
                            break
                except:
                    print(" - no word recognized!")

    def commandRoutine(self):
        duration = 10
        r = sr.Recognizer()
        with sr.Microphone() as source:
        #with sr.Microphone(device_index=6) as source:
            # read the audio data from the default microphone
            print("    - Please speak for",duration, "seconds ...")
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source, duration=duration)
            #print(" - Recognizing...")
            # convert speech to text
            #text = r.recognize_google(audio_data)
            text = None

            #text = r.recognize_google(audio_data, language="en-EN")
            #self.lampiGrammar(text)
            try:
                text = r.recognize_google(audio_data, language="en-EN")
                return_val = self.read_text(text)
                self.lampiGrammar(text)
                
                '''
                if return_val==1:
                    self.lampiGrammar(text)
                else:
                '''

                #print("    - heard: ",text)
            except:
                pygame.init()
                pygame.mixer.music.load('did_not_hear.mp3')
                pygame.mixer.music.play()
                time.sleep(5)
                pygame.mixer.music.fadeout(5)

                print("    - no command recognized!")
            
    def read_text(self,text):
        #print("read text")
        #print(str(text))

        language = 'en'
        myobj = gTTS(text=str(text), lang=language, slow=False) 

        myobj.save("read_command.mp3") 
        pygame.init()

        pygame.mixer.music.load('I_heard.mp3')
        pygame.mixer.music.play()
        time.sleep(1)

        pygame.mixer.music.load('read_command.mp3')
        pygame.mixer.music.play()
        time.sleep(5)

        pygame.mixer.music.load('is_this_correct.mp3')
        pygame.mixer.music.play()
        time.sleep(2)

        pygame.mixer.music.fadeout(5)

        reply_falg = True

        duration = 2
        r = sr.Recognizer()
        while(reply_falg!=False):
            with sr.Microphone() as source:
            #with sr.Microphone(device_index=6) as source:
                # read the audio data from the default microphone
                print("    - Please speak for",duration, "seconds ...")
                r.adjust_for_ambient_noise(source)
                audio_data = r.record(source, duration=duration)
                #print(" - Recognizing...")
                # convert speech to text
                #text = r.recognize_google(audio_data)
                text = None
                
                #text = r.recognize_google(audio_data, language="en-EN")
                #self.lampiGrammar(text)
                try:
                    text = r.recognize_google(audio_data, language="en-EN")
                    text = text.split(" ")
                    if "yes" in text or "Yes" in text:
                        reply_falg = False
                        return 1
                    if "no" in text or "No" in text:
                        reply_falg = False
                        return 0
                    #print("    - heard: ",text)
                except:
                    pygame.init()
                    pygame.mixer.music.load('say_again.mp3')
                    pygame.mixer.music.play()
                    time.sleep(5)
                    pygame.mixer.music.fadeout(4)

                    print("    - no command recognized!")





    def lampiGrammar(self,text):
        #print("lampi grammar")
        print("    - heard: ",text)
        #print(text)
        
        if "set" or "Set" in str(text):
            self.setGrammar(text)
        if "turn" or "Turn" in str(text):
            self.turnGrammar(text)
        
        self.publish_config_change()

    def turnGrammar (self,text):
        print("    - turn grammar")
        command = str(text)
        command = command.split(" ")
        #print(command)
        turn_list = ["on", "off"]

        turn_flag = False
                
        for word in command:
            #print(word)
            if "turn"==word or "Turn"==word:
                print("set flag true")
                turn_flag = True
            if turn_flag:
                if word.lower() in turn_list:
                    if  word.lower() == "on":
                        print("Turn on")
                        self.on_off= True
                        break
                    if word.lower() == "off":
                        print("Turn off")
                        self.on_off= False
                        break
        


    def setGrammar (self,text):
        print("    - set grammar")

        set_list = ["hue", "saturation", "brightness"]
        color_list = ["red","green","blue","yellow"]

        Dict = dict({"hue": None, "saturation": None, "brightness": None, "color":None}) 

        #mqtt_dict = dict({"hue": None, "saturation": None, "brightness": None}) 

        command = str(text)
        command = command.split(" ")
        #print(command)

        set_flag = False
                
        i = 0
        ii = 0
        color_flag_error = False

        hsv_flag = False
        rbg_flag = False
        temp = []
        for word in command:
            #print(word)
            if "set"==word or "Set"==word:
                #print("set flag true")
                set_flag = True
            if set_flag:
                if word.lower() in set_list: 
                    temp.append(word.lower())
                    #print("   added", word)

                if word.lower() in color_list:
                    if Dict["color"] != None:
                        print("error. too many colors. ")
                        color_flag_error = True
                    Dict["color"]=word.lower() 
                    #print("   added", word)

                if "%" in word:
                    digit = word.split("%")
                    digit = float(digit[0])
                    for item in temp:
                        #print("         ",item)
                        if item == "hue":
                            Dict["hue"] = digit/100
                            hsv_flag = True
                        if item == "saturation":
                            Dict["saturation"] = digit/100
                            hsv_flag = True
                        if item == "brightness":
                            Dict["brightness"] = digit/100
                    temp = []


        #print(command)
        if (Dict["color"]) !=None and (Dict["hue"]!=None and Dict["saturation"]!=None):
            print("error")
        elif Dict["color"]!=None:
            if Dict["color"] == "red":
                #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
                (hue, saturation,value) = colorsys.rgb_to_hsv(255, 0, 0)
            elif Dict["color"] == "green":
                #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
                (hue, saturation,value) = colorsys.rgb_to_hsv(0, 255, 0)
            elif Dict["color"] == "blue":
                #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
                (hue, saturation,value) = colorsys.rgb_to_hsv(0, 0, 255)
            elif Dict["color"] == "yellow":
                #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
                (hue, saturation,value) = colorsys.rgb_to_hsv(255, 255, 0)

            if color_flag_error == False:
                Dict["hue"] = hue
                Dict["saturation"] = saturation
                #print("    - Set:","hue:",hue,"saturation:",saturation,"brightness:",brightness)
                #self.publish_config_change(Dict)
                # write data

        elif Dict["hue"]!=None or Dict["saturation"]!=None :
            hue = Dict["hue"]
            saturation = Dict["saturation"]
            brightness = Dict["brightness"]

        if Dict["hue"]!=None:
            self.hue = Dict["hue"]
        if Dict["saturation"]!=None:
            self.saturation = Dict["saturation"]
        if Dict["brightness"]!=None:
            self.brightness = Dict["brightness"]

    def publish_config_change(self):
        config = {'color': {'hue':self.hue, 'saturation':self.saturation},
                  'brightness': self.brightness,
                  'on': self.on_off,
                  'client': 'local'}

        print("    - mqtt send :",config)


def main():
    lampi_speech = LampiSpeech()
    lampi_speech.listenRoutine()


if __name__ == "__main__":
    main()

