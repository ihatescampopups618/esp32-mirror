hello felow person who wants their tiny clone st7735s to become their monitor heres how to run it
Step 1:
get all the requireed libraries:
you will need:

Arduino IDE:
TFT_eSPI (by Bodmer)
Adafruit ST7735
Adafruit GFX

Python (PC):
mss
opencv-python (imported as cv2)
numpy
pyserial (imported as serial)
(you can install these by simply typing "pip install mss opencv-python numpy pyserial" on your command promt)
wire your esp32 to the display:
SDA / MOSI > Pin 23
SCL / SCLK > Pin 18
CS > Pin 5
DC > Pin 4
RES / RST > Pin 26
VCC > 3.3V / 5V
GND > GND
Step 2:
you'll need arduino IDE for this one
compile the file "client.ino" to your esp32
Step 3:
now, copy the User_Setup.h file then open up your Arduino folder (usually located at "C:\Users\[YOUR_USERNAME\Documents\Arduino"
 and click on "libraries" then click on "TFT_eSPI" then paste the file, click on "Replace file in destination" and
 now, open up your command promt, cd (change diretory) to your "esp32_mirror" folder and then run "python server.py"
remember to copy and not manualy write the command.
Step 4:
Now that everything is running your mini monitor should be working! 
