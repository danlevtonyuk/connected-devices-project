# connected-devices-project

## Bluetooth Module
Bluetooth script receives data on serial port, parses data, and extracts Ax, Ay, and Az which are the three acceleration axis.

It computes roll and pitch from the three parameters.

## Speech to Text Module
Speech to text module takes input voice from user (default computer mic) and extract text from.

It requires the following libraries to be installed:

```python
pip install SpeechRecognition
```

It takes a list of inputs and if the word "Lampi" or "listen" is detected, it exists the program. 
