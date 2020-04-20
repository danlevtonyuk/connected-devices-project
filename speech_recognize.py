import speech_recognition as sr
import colorsys


class LampiSpeech(object):
    def __init__(self):
        #pass

        self.hue = 1.0
        self.brightness = 1.0
        self.saturation = 1.0
        self.on_off = True
        
        # get values from mqtt
        

    def listenRoutine(self):
        r = sr.Recognizer()
        list_text = ['a lumpy','hey Lumpy', 'lamp', 'Halen', 'Hayden', 'listen', 'Listen', 'Lampe', 'lampe']
        stop_flag = True
        duration = 3
        while(stop_flag):
            config = {'color': {'hue':self.hue, 'saturation':self.saturation},
                  'brightness': self.brightness,
                  'on': self.on_off,
                  'client': 'local'}
        
            print("    - mqtt saved:",config)

            with sr.Microphone() as source:
            #with sr.Microphone(device_index=6) as source:
                # read the audio data from the default microphone
                print(" - Call lampi (",duration, "seconds ) ...")
                r.adjust_for_ambient_noise(source)
                audio_data = r.record(source, duration=duration)
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
                self.lampiGrammar(text)
                #print("    - heard: ",text)
            except:
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
        
            #print("    - Set:","hue:",hue,"saturation:",saturation,"brightness:",brightness)
            
            #self.publish_config_change(Dict)
        
        if Dict["hue"]!=None:
            self.hue = Dict["hue"]
        if Dict["saturation"]!=None:
            self.saturation = Dict["saturation"]
        if Dict["brightness"]!=None:
            self.brightness = Dict["brightness"]

        #self.write_mqtt(Dict)
    
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

