# Chatpad-Python
Python script for converting Chatpad data into text via UART connection

This is a Python script used to convert Xbox360 Chatpad inputs over UART into readable code using the "Keyboard" Python module.

Limitations:
Shift and Orange keys work, but Green and Capslock do not.
Key inputs can lag and cause typos.
When loaded at boot Python script sometimes does not "wake up" the chatpad and has to be rebooted.
More than two keypresses of normal ASCII keys is not currently supported due to primitive "debouncing" of incoming data.

I believe all of the above can be corrected by coders better than myself at Python.

Currently when Green+(Button) are pressed the Keyboard module reports that "X" is not a defined key. Even when that key is present on the keyboard.

This software is distributed as-is and you can edit it and distribute it as you like.
