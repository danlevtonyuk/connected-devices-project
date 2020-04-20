import colorsys

text_1 =  "set brightness and Saturation to 20% and hue to 30%"

text_2 = "Set Brightness to 10% hue to 20% and saturation to 30%"

text_3 = "set brightness saturation and Hue to 20%"

text_4 =  "set brightness to 20% and color to red"

text_5 =  "set brightness to 100% and color to red"

text_6 =  "set brightness to 100% and color to red and green"

text_7 =  "set color to red and brightness to 10%"

text_20 =  "set brightness and Saturation to 20% and hue to 30% red"

set_list = ["hue", "saturation", "brightness"]
color_list = ["red","green","blue","yellow"]

Dict = dict({"hue": None, "saturation": None, "brightness": None, "color":None}) 



command = text_7
command = command.split(" ")

set_flag = False
        
i = 0
ii = 0
color_flag_error = False

hsv_flag = False
rbg_flag = False
temp = []
for word in command:
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
        if "%" in word:
            digit = word.split("%")
            digit = float(digit[0])
            for item in temp:
                if item == "hue":
                    Dict["hue"] = digit/100
                    hsv_flag = True
                if item == "saturation":
                    Dict["saturation"] = digit/100
                    hsv_flag = True
                if item == "brightness":
                    Dict["brightness"] = digit/100
            temp = []


print(command)
if (Dict["color"]) !=None and (Dict["hue"]!=None and Dict["saturation"]!=None):
    print("error")
elif Dict["color"]!=None:
    if Dict["color"] == "red":
        #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
        (hue, saturation,value) = colorsys.rgb_to_hsv(255, 0, 0)
        brightness = Dict["brightness"]
    elif Dict["color"] == "green":
        #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
        (hue, saturation,value) = colorsys.rgb_to_hsv(0, 255, 0)
        brightness = Dict["brightness"]
    elif Dict["color"] == "blue":
        #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
        (hue, saturation,value) = colorsys.rgb_to_hsv(0, 0, 255)
        brightness = Dict["brightness"]
    elif Dict["color"] == "yellow":
        #print(colorsys.rgb_to_hsv(int(255*float(Dict["brightness"])), 0, 0))
        (hue, saturation,value) = colorsys.rgb_to_hsv(255, 255, 0)
        brightness = Dict["brightness"]

    if color_flag_error == False:
        print("hue:",hue,"saturation:",saturation,"brightness:",brightness)
        # write data

elif Dict["hue"]!=None or Dict["saturation"]!=None :
    hue = Dict["hue"]
    saturation = Dict["saturation"]
    brightness = Dict["brightness"]
   
    print(hue,saturation,brightness)

#print(Dict)
#color_flag_error = False

                    



        
