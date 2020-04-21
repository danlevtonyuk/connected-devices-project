from gtts import gTTS 
import os 
  
mytext = 'Welcome to geeksforgeeks!'
  
language = 'en'
  
myobj = gTTS(text=mytext, lang=language, slow=False) 
  
myobj.save("welcome.mp3") 
  
import pygame, time
pygame.init()
pygame.mixer.music.load('welcome.mp3')
pygame.mixer.music.play()
time.sleep(5)
pygame.mixer.music.fadeout(5)