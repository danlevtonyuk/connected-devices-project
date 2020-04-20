# connected-devices-project

## Bluetooth Module
Bluetooth script receives data on serial port, parses data, and extracts Ax, Ay, and Az which are the three acceleration axis.

It computes roll and pitch from the three parameters.

## Speech to Text Module
Speech to text module takes input voice from user (default computer mic) and extract text from.

It requires the following libraries to be installed:

```python
sudo pip install SpeechRecognition
sudo apt-get install python-pyaudio python3-pyaudio
```

It takes a list of inputs and if the word "Lampi" or "listen" is detected, it exists the program. 

This is a good source as an instruction on text to speech library:
https://realpython.com/python-speech-recognition/

### How to use:
It takes an input voice for 5 seconds which should include either lampi or listem or both.

Then it listens for 10 to 15 seconds (you can set in the code) and then generates a texts and makes proper mqtt command.
