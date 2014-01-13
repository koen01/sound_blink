# Adapted for blinkstick. Code and idea from http://julip.co/2012/03/arduino-python-soundlight/
 
import pyaudio # from http://people.csail.mit.edu/hubert/pyaudio/
import serial  # from http://pyserial.sourceforge.net/
import audioop
import sys
import math
from blinkstick import blinkstick
bstick = blinkstick.find_first()
if bstick is None:
    print "No BlinkSticks found..."

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i)+'. '+dev['name']
        i += 1
 
def blinkstick_soundlight():
    chunk    = 1024 # Change if too fast/slow, never less than 1024
    scale    = 30   # Change if too dim/bright
    exponent = 1    # Change if too little/too much difference between loud and quiet sounds
 
    # CHANGE THIS TO CORRECT INPUT DEVICE
    # Enable stereo mixing in your sound card
    # to make you sound output an input
    # Use list_devices() to list all your input devices
    device   = 0
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)
    
    print "Starting, use Ctrl+C to stop"
    try:
        while True:
            data  = stream.read(chunk)
            rms   = audioop.rms(data, 2)
            level = min(rms / (2.0 ** 16) * scale, 1.0) 
            level = level**exponent 
            level = int(level * 255) 
            print level
 	    bstick.set_color(25, 255 - level, 80)	
    except KeyboardInterrupt:
        pass
    finally:
        print "\nStopping"
	stream.close()
        p.terminate()
        bstick.turn_off()
if __name__ == '__main__':
    list_devices()
    blinkstick_soundlight()
