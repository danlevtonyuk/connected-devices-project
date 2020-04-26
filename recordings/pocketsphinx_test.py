import os
from pocketsphinx import pocketsphinx, Jsgf, FsgModel, AudioFile, get_model_path, get_data_path
from IPython import embed


def decode_phrase(decoder, wav_file):
    decoder.start_utt()
    stream = open(wav_file, "rb")
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
    decoder.end_utt()
    words = []
    [words.append(seg.word) for seg in decoder.seg()]
    return words



grammar_file = 'lampi_text_for_detection_complex'  # do not use any extension for this file
model_path = get_model_path() # 'speech_recognizing/lib/pocketsphinx/'
language = 'en-US'

grammar_path = os.path.join(os.getcwd(), grammar_file)
fsg_path1 = "{}1.fsg".format(grammar_path)

print("Grammar Filepath: {}".format(grammar_path))
print("FSG Grammar Filepath: {}".format(fsg_path1))

# Create decoder object
config = pocketsphinx.Decoder.default_config()
config.set_string("-hmm", os.path.join(model_path, language))
config.set_string("-lm", os.path.join(os.getcwd(), "TAR1172", '1172.lm'))
config.set_string("-dict", os.path.join(os.getcwd(), "TAR1172", '1172.dic'))
decoder = pocketsphinx.Decoder(config)

# Compile Grammar File
jsgf = Jsgf(grammar_path + ".jsgf")

rule_string1 = "my_lampi.action" # "{0}.{0}".format(grammar_file)

print("rule_string:", rule_string1)
rule1 = jsgf.get_rule(rule_string1)

fsg1 = jsgf.build_fsg(rule1, decoder.get_logmath(), 7.5)

print("The Path: ", fsg_path1, fsg1)

fsg1.writefile(fsg_path1)

# Set grammar to decoder
decoder.set_fsg(fsg_path1, fsg1)
print("setting grammar file:", grammar_file)
print("current search:", decoder.get_search())
#embed()
#decoder.set_search("my_lampi")
temp = decode_phrase(decoder, "SplitUp/all_sentences_00_16k.wav")
print(temp)
#embed()

def parse_words(inputw):
    # first, parse out the things I don't want:
    iw = []
    for word in inputw:
      if word != '<s>' and word != '<sil>' and word != '[SPEECH]' and word != '</s>':
        iw += [word]
    if iw[0] == 'LAMPI':
      if iw[1] == "TOGGLE":
        # toggle on/off - means I have to know current state!
        print("You want to toggle power")
      elif iw[1] in set(['SET', 'TURN', 'CHANGE']):
        if iw[2] in set(['HUE', 'SATURATION', 'BRIGHTNESS']):
      else:
        print("Could not parse sentence1!", iw)

    elif iw[0] == 'HEY' and iw[1] == "LAMPI":
    else:
      print("Could not parse sentence2!", iw)
      










