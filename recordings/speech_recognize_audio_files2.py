#!/usr/bin/python3
import speech_recognition as sr
import colorsys
import pygame, time
from gtts import gTTS
import os
import pyaudio
from datetime import datetime
from pocketsphinx import AudioFile, get_model_path, get_data_path
import sys
from lampi_sphinx_app import SphinxApp
import pipreqs
import pyttsx3
from IPython import embed

files = os.listdir(os.path.join(os.getcwd(), "SplitUp"))

def getaudiodevices():
    p = pyaudio.PyAudio()
    print("audio devices", p.get_device_count(), flush=True)
    for i in range(p.get_device_count()):
        name_i = p.get_device_info_by_index(i).get('name')
        print("name_i:", name_i, name_i.find("PnP"), flush=True)
        print(p.get_device_info_by_index(i).get('name'), flush=True)
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
        self.LampSphinxService = SphinxApp()
        self.LampSphinxService.on_start()
        self.speech_engine = pyttsx3.init()
        self.speech_engine.setProperty('voice', 'en-american')
        self.speech_engine.setProperty('rate', '100')
        self.speech_engine.say('Lampi is online')
        self.speech_engine.runAndWait()
        self.speech_engine.stop()
        pygame.init()

    def listenRoutine(self):
        r = sr.Recognizer()
        duration = 5
        listen_timestamp = 0

        our_device = getaudiodevices()
        print("Detected our mic:", our_device, flush=True)
        with sr.Microphone(device_index=our_device, sample_rate=48000) as source:
            r.adjust_for_ambient_noise(source, duration=5)
            temp = r.energy_threshold
            r.dynamic_energy_threshold = False
            r.energy_threshold = temp + 50
            while (1):
                print("Energy threshold:", temp+50)
                pygame.mixer.music.load("cartoon_wink.wav")
                pygame.mixer.music.play()
                print("Pi is listening! Speak... [Last loop took:%s]" % (time.clock() - listen_timestamp), flush=True)
                audio_data = r.listen(source, timeout=None)
                #audio_data = r.record(source, duration=duration)
                listen_timestamp = time.clock()
                pygame.mixer.music.load('ding_.wav')
                pygame.mixer.music.play()
                print("Pi captured! Processing...", flush=True)
                try:
                    # text = r.recognize_google(audio_data, language="en-EN")
                    #sphinx_dec = r.recognize_sphinx(audio_data, language="en-US", grammar="my_lampi.jsgf") # , show_all=True)
                    #sphinx_dec = r.recognize_sphinx(audio_data, language="en-US", grammar="OurDictionary.jsgf") # , show_all=True)
                    sphinx_dec = r.recognize_sphinx(audio_data, language=("/home/pi/.local/lib/python3.5/site-packages/pocketsphinx/model/en-us", "/home/pi/final_project/connected-devices-project/recordings/OurDictionary/OurDictionary.lm", "/home/pi/final_project/connected-devices-project/recordings/OurDictionary/OurDictionary.dict"), grammar="OurDictionary.jsgf") # , show_all=True)
                    #grammar = ("/home/pi/.local/lib/python3.5/site-packages/pocketsphinx/model/en-us", "/home/pi/final_project/connected-devices-project/recordings/OurDictionary/OurDictionary.lm", "/home/pi/final_project/connected-devices-project/recordings/OurDictionary/OurDictionary.dic")
                    # print("\n\n\nSphinx:" + sphinx_dec, flush=True)

                    commands = detect_language(sphinx_dec)
                    print("commands:", commands)
                    self.LampSphinxService.update_new_config(commands)
                except Exception as exc:
                  print(exc, flush=True)


        exit()
        for each_file in files:
            print(each_file)
            with sr.AudioFile(os.path.join(os.getcwd(), "SplitUp", each_file)) as source2:
              recording = r.record(source2)
              #print("Google:", r.recognize_google(recording, language="en-US", show_all=True))
              # - print("Google with key:", r.recognize_google(recording, key="AIzaSyCMGSGwceDWKdNAtZE4m5ATxvj7ryoFRMU", language="en-US", show_all=True))

              #print("Google cloud:", r.recognize_google_cloud(recording, credentials_json=open("My First Project-fbdc14cb6af3.json", "r").read(), language="en-US", show_all=True))

              #sphinx_dec = r.recognize_sphinx(recording, language="en-US", keyword_entries=words_to_detect, grammar="lampi_text_for_detection.jsgf")#, show_all=True)
              sphinx_dec = r.recognize_sphinx(recording, language="en-us", grammar="lampi_text_for_detection_complex2.jsgf") # , show_all=True)
              # print("\n\n\nSphinx:" + sphinx_dec)

              commands = detect_language(sphinx_dec)
              self.LampService.update_new_config(commands)

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

class LanguageProcessor:
    def __init__(self):
        self.ColorMap = {"RED":        {"h":0.00, "s":1.0},
                         "ORANGE":     {"h":0.08, "s":1.0},  #  30*, 100%
                         "YELLOW":     {"h":0.16, "s":1.0},  #  60*, 100%
                         "GREEN":      {"h":0.33, "s":1.0},  # 120*, 100%
                         "BLUE":       {"h":0.66, "s":1.0},  # 240*, 100%
                         "PURPLE":     {"h":0.83, "s":1.0},  # 300*, 100%
                         "MAGENTA":    {"h":0.83, "s":1.0},  # 300*, 100%
                         "TAN":        {"h":0.09, "s":0.34}, #  34*,  34%
                         "CYAN":       {"h":0.50, "s":1.0},  # 180*, 100%
                         "AQUAMARINE": {"h":0.44, "s":0.50}, # 160*,  50%
                         "PINK":       {"h":0.97, "s":0.25}, # 350*,  25%
                         "WHITE":      {"h":0.00, "s":0.00}, #   0*,   0%
                        }
        self.NumberMap = {"ZERO":'0', "ONE":'1', "TO": '2',  "TWO":'2', "THREE":'3', "FOUR":'4', "FIVE":'5', "SIX":'6', "SEVEN":'7', "EIGHT":'8', "NINE":'9', "POINT":'.'}
        self.nested = 0
    def start(self, word, words):
        if not len(words): return word
        self.nested = 1
        if words[0] == "HEY":     return self.Hey(word, words[1:])
        elif words[0] == "LAMPI": return self.Lampi(word + "[ LAMPI", words[1:])
        elif self.nested:
            if words[0] == "HUE":        return self.Hue(word + " HUE { 'h':", words[1:   ])
            if words[0] == "SATURATION": return self.Saturation(word + " SATURATION { 's':", words)
            if words[0] == "BRIGHTNESS": return self.Brightness(word + " BRIGHTNESS {'b':", words)
        return self.start(word + " / ", words[1:])
    def Hey(self, word, words):
        if words[0] == "LAMPI": return self.Lampi(word + "[ LAMPI", words[1:])
        return self.start(word + " / ", words[1:])
    def Lampi(self, word, words):
        if words[0] in ["SET", "CHANGE", "TURN"]: return self.Set(word + " SET", words[1:])
        elif words[0] == "TOGGLE":                return self.Toggle(word + " TOGGLE", words[1:])
        return self.start(word + " / ", words[1:])
    def Set(self, word, words):
        if not len(words):           return word
        if words[0] == "THE":        return self.Set(word, words[1:]) # remove additional "the"s
        if words[0] == "TO":         return self.Set(word, words[1:])
        if words[0] == "HUE":        return self.Hue(word + " HUE { 'h':", words[1:])
        if words[0] == "SATURATION": return self.Saturation(word + " SATURATION { 's':", words[1:])
        if words[0] == "BRIGHTNESS": return self.Brightness(word + " BRIGHTNESS {'b':", words[1:])
        if words[0] == "LAMP":       return self.Power(word + " POWER", words[1:])
        if words[0] == "POWER":      return self.Power(word + " POWER", words[1:])
        if words[0] == "OFF":        return self.Power(word + " POWER", words)
        if words[0] == "ON":         return self.Power(word + " POWER", words)
        if words[0] == "COLOR":      return self.Color(word + " COLOR", words[1:])
        return self.start(word + " / ", words[1:])
    def Hue(self, word, words):
        if not len(words): return word
        if words[0] == "TO":                        return self.Hue(word, words[1:]) # remove additional "TO"s
        else: # detect a color or a number
            if words[0] in self.ColorMap.keys():    return self.Color(word, words) # acceptable colors
            elif words[0] in self.NumberMap.keys(): return self.Number(word, words) # acceptable numbers
        return self.start(word + " / ", words)
    def Saturation(self, word, words):
        if not len(words): return word
        if words[0] == "TO":                      return self.Saturation(word, words[1:]) # remove additional "TO"s
        else: # detect a color or a number
            if words[0] in self.NumberMap.keys(): return self.Number(word, words) # acceptable numbers
        return self.start(word + " / ", words[1:])
    def Brightness(self, word, words):
        if not len(words): return word
        if words[0] == "TO":                      return self.Brightness(word, words[1:]) # remove additional "TO"s
        else: # detect a color or a number
            if words[0] in self.NumberMap.keys(): return self.Number(word, words) # acceptable numbers
            if words[0] == "OFF": return self.start(word + " 0 ] /", words[1:])
        return self.start(word + " / ", words[1:])
    def Power(self, word, words):
        if words[0] == "TO": return self.Power(word, words[1:])
        else: # detect ON/OFF
            if words[0] == "ON": return self.start(word + " 1 ] / ", words[1:])
            elif words[0] == "OFF": return self.start(word + " 0 ] / ", words[1:])
            return self.start(word + " 1 ] / ", words)
        return self.start(word, words)
    def Toggle(self, word, words):
        if not len(words): return word + " ] / "
        return self.start(word + " ] / ", words[1:])
    def Color(self, word, words):
        if not len(words): return word
        if words[0] == "TO" : return self.Color(word, words[1:])
        if words[0] in self.ColorMap.keys(): return self.start(word + " " + str(self.ColorMap[words[0]]) + " ] / ", words[1:])
        return self.start(word + " / ", words[1:])
    def Number(self, word, words):
        parsed_number = ''
        index = 0
        while index < len(words) and words[index] in self.NumberMap.keys():
            parsed_number += self.NumberMap[words[index]]
            index += 1
            if index == len(words):
                if words[index-1] != "POINT":
                    return self.start(word + " " + parsed_number + " } ] / ", words[index:])
                return self.start(word + " " + parsed_number + " / ", words[index:])
        return self.start(word + " " + parsed_number + " } ] / ", words[index:])

def eval_command(command):
    try:
        #print("Trying to eval command", command, flush=True)
        interpreted = eval(command)
        #print("interpreted:", interpreted, flush=True)
        return interpreted
    except Exception as exc:
        #print("got exc from eval:", exc, flush=True)
        return command


global_times = []
def detect_language(input_words):
    global global_times
    print("DETECT LANGUAGE!", input_words)
    words = input_words.split(" ")
    p = LanguageProcessor()
    time_start = time.clock()
    processed = p.start('', words)
    # print(processed, flush=True)
    commands = processed.split("/")
    final = []
    for command in commands:
        #print("commandA", command)
        if command.find("[") != -1:
            if command.find("]") != -1:
                if command != '':
                    if command != ' ':
                        #print("commandB", command)
                        #print("command.split 1", command.split("["))
                        command = command.split("[")[1:]
                        command = "".join(command)
                        #print("command.split 2", command.split("]"))
                        command = command.split("]")[:-1]
                        command = "".join(command)
                        #print("commandC", command)
                        if command.count("{") == command.count("}"):
                            if command.find("{") != -1:
                                temp = "{" + command.split("{")[1]
                                temp = temp.split("}")[0] + "}"
                                final += [eval_command(temp)]
                            else:
                                final += [eval_command(command)]

    # print("final", final, flush=True)
    time_end = time.clock()
    global_times += [time_end-time_start]
    # print(global_times, sum(global_times), len(global_times), flush=True)
    return final

def main():
    lampi_speech = LampiSpeech()
    lampi_speech.listenRoutine()


if __name__ == "__main__":
    main()

