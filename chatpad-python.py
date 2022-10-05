import time
import serial
import keyboard
import threading

keyModsDict = {
    b'\x01': 'shift',
    b'\x02': 'green',
    b'\x04': 'orange',
    b'\x08': 'people',
    b'\x05': 'caps'
};

primeKeysDict = {
    # Numbers
    b'\x17': '1',
    b'\x16': '2',
    b'\x15': '3',
    b'\x14': '4',
    b'\x13': '5',
    b'\x12': '6',
    b'\x11': '7',
    b'\x67': '8',
    b'\x66': '9',
    b'\x65': '0',
    # Letters
    b'\x37': 'a',
    b'\x42': 'b',
    b'\x44': 'c',
    b'\x35': 'd',
    b'\x25': 'e',
    b'\x34': 'f',
    b'\x33': 'g',
    b'\x32': 'h',
    b'\x76': 'i',
    b'\x31': 'j',
    b'\x77': 'k',
    b'\x72': 'l',
    b'\x52': 'm',
    b'\x41': 'n',
    b'\x75': 'o',
    b'\x64': 'p',
    b'\x27': 'q',
    b'\x24': 'r',
    b'\x36': 's',
    b'\x23': 't',
    b'\x21': 'u',
    b'\x43': 'v',
    b'\x26': 'w',
    b'\x45': 'x',
    b'\x22': 'y',
    b'\x46': 'z',
    # Punctuation
    b'\x53': '.',
    b'\x62': ',',
    #Control
    b'\x63': '\n',
    b'\x71': '\b',
    b'\x54': ' ',
    b'\x08': 'windows',
    b'U': 'left',
    b'Q': 'right'
}

greenKeysDict = {
    # Letters
    b'\x37': '~',
    b'\x42': '|',
    #44: 'c',
    b'\x35': '{',
    b'\x25': '€',
    b'\x34': '}',
    #33: 'g',
    b'\x32': '/',
    b'\x76': '*',
    b'\x31': '\'',
    b'\x77': '[',
    b'\x72': ']',
    b'\x52': '>',
    b'\x41': '<',
    b'\x75': '(',
    b'\x64': ')',
    b'\x27': '!',
    b'\x24': '#',
    #36: 's',
    b'\x23': '%',
    b'\x21': '&',
    b'\x43': '-',
    b'\x26': '@',
    b'\x45': 'x',
    b'\x22': '^',
    b'\x46': '`',
    # Punctuation
    b'\x53': '?',
    b'\x62': ':',
    b'\x08': 'ctrl'
}

orangeKeysDict = {
    # Letters
    #37: 'a',
    b'\x42': '+',
    #44: 'c',
    #35: 'd',
    #25: 'e',
    #34: 'f',
    #33: 'g',
    b'\x32': '\\',
    #76: 'i',
    b'\x31': '"',
    #77: 'k',
    #72: 'l',
    #52: 'm',
    #41: 'n',
    #75: 'o',
    b'\x64': '=',
    #27: 'q',
    b'\x24': '$',
    #36: 's',
    #23: 't',
    #21: 'u',
    b'\x43': '_',
    #26: 'w',
    #45: 'x',
    #22: 'y',
    #46: 'z',
    # Punctuation
    #53: '.',
    b'\x62': ';',
    b'\x08': 'alt',
    b'U': 'up',
    b'Q': 'down'
}

#port_name = "COM3" #For Windows testing
port_name = "/dev/ttyUSB0" #For CyberCon use

chatPad_Init = b'\x87\x02\x8C\x1F\xCC'
chatPad_Wake = b'\x87\x02\x8C\x1B\xD0'
chatPad_DataLength = 8

#Set the port and speeds
ser = serial.Serial(
    port=port_name,
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    )
#print(ser.is_open)
#This constantly pokes the chatpad to keep it awake
def keepAwake():
    threading.Timer(0.5, keepAwake).start()
    ser.write(chatPad_Wake)

keepAwake()

#Writ the init to the chat pad
ser.write(chatPad_Init)
keyBytes = []
startEncode = False
keyPressed = False
shiftPressed = False
capsPressed = False
capsOn = False
orangePressed = False
greenPressed = False
#Get the key presses from the chatpad
while True:
    msg = ser.read()
    if msg == b'\xa5' and startEncode == False: #Wait for the first status code to perform bit-alignment
        startEncode = True
    if startEncode == True:
        keyBytes.append(msg)
    if len(keyBytes) == 8:
        if keyPressed == True and keyBytes[4] == b'\x00':
            keyPressed = False
        if keyBytes[4] != b'\xa5': #Ensures that the first byte is status byte
            if keyBytes[3] == b'\x01':
                shiftPressed = True
            elif keyBytes[3] == b'\x02':
                greenPressed = True
            elif keyBytes[3] == b'\x04':
                orangePressed = True
            elif keyBytes[7] == b'\x87':
                winPressed = False
                shiftPressed = False
                greenPressed = False
                orangePressed = False
                specialPressed = False

            #Capslock is special and is being hit multiple times. Needs similar single keypress as regular keys, but isn't working?
            #if keyBytes[7] == b'\x82':
                #keyboard.press("caps_lock")
            #else:
                #keyboard.release("caps_lock")

            if greenPressed == True:
                keyMap = greenKeysDict
            elif orangePressed == True:
                keyMap = orangeKeysDict
            else:
                keyMap = primeKeysDict
            for key, value in keyMap.items():
                if keyBytes[4] == key: #or keyBytes[3] == b'\x08': #This creates a tuples out of range error for "windows" key
                    if keyPressed == False:
                        keyboard.press_and_release(value)
                        keyPressed = True
            print(keyBytes)
            keyBytes = []
        elif keyBytes[4] == b'\xa5':
            keyBytes = []
            startEncode = False
    if shiftPressed == True:
        keyboard.press('shift')
    else:
        keyboard.release('shift')

# After measurements are done, close the connection
ser.close()
