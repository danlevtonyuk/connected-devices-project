from gtts import gTTS 
import os 
  
mytext = 'I didnt get that. Please say again!'
  
language = 'en'
  
myobj = gTTS(text=mytext, lang=language, slow=False) 
  
myobj.save("say_again.mp3") 
  
import pygame, time
pygame.init()
pygame.mixer.music.load('say_again.mp3')
pygame.mixer.music.play()
time.sleep(5)
pygame.mixer.music.fadeout(5)