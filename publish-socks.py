import time
import threading
time.sleep(60)
import paho.mqtt.client as paho
import board
import neopixel
import datetime
pin = board.D18
pix = 300

pixels = neopixel.NeoPixel(pin, pix, brightness=1, auto_write=False)
broker="192.168.1.200"
clock = False
running = False
backlight = False
duration = 20

def clockOff(x):
   global clock
   global running
   if not x:
      clock = False
   
   if running == True:
      running = False
      time.sleep(1)  
   pixels.fill((0,0,0))
   pixels.show()

#Light functions
def frontWhite():
   for i in range (36):
      pixels[i] = (255,255,255)
   pixels.show()

def red():
   clockOff(0)
   for i in range (36,72):
      pixels[i] = (255,112,60)
   #pixels.fill((255,0,0))
   frontWhite()

def green():
   clockOff(0)
   pixels.fill((0,255,0))
   frontWhite()

def blue():
   clockOff(0)
   pixels.fill((0,0,255))
   frontWhite()

def orange():
   clockOff(0)
   pixels.fill((255,128,0))
   frontWhite()

def whiteOn():
   clockOff(0)
   pixels.fill((255,255,255))
   pixels.show()

def timeOn():
   clockOff(1)
   setTime()

def backlight_fade():
   global duration
   global running
   global backlight
   decimal = 1/duration*255
   r = 0
   g = 255
   for x in range (duration+1):
      if r <= 255 and g >= 0 and running:
         for i in range (36,72):
            pixels[i] = (r,g,0)
         pixels.show()
      else:
         break
      r += decimal
      g -= decimal
      print("red: ",r,", green : ",g)
      time.sleep(0.95)
   backlight = False


def geese():
   clockOff(0)
   global running
   running = True
   global backlight
   backlight = True
   s = 0.05
   b = threading.Thread(target=backlight_fade)
   b.start()

   while backlight:
      for i in range (1,13):
         if running:
            pixels[i*3-1] = pixels[i*3-2] = pixels[i*3-3] = (255,255,255)
            pixels.show()
            time.sleep(s)

      for i in range (1,13):
         if running:
            pixels[i*3-1] = pixels[i*3-2] = pixels[i*3-3] = (0,0,0)
            pixels.show()
            time.sleep(s)

   if running:
      for i in range (4):
         for x in range (36):
            pixels[x] = (255,255,255)
         pixels.show()
         time.sleep(0.5)
         for x in range(36):
            pixels[x] = (0,0,0)
         if i == 3:
            pixels.fill((0,0,0))
         pixels.show()
         time.sleep(0.5)

def goose():
   clockOff(0)
   global running
   running = True
   s = 0.05
   for i in range (36,72):
      pixels[i] = (255,112,60)
   for x in range(10):
      for i in range (1,13):
         if running:
            pixels[i*3-4] = pixels[i*3-5] = pixels[i*3-6] = (0,0,0)
            pixels[i*3-1] = pixels[i*3-2] = pixels[i*3-3] = (255,255,255)
            pixels.show()
            time.sleep(s)
            if i == 12:
               pixels[i*3-1] = pixels[i*3-2] = pixels[i*3-3] = (0,0,0)
               pixels.show()
         else:
            break

#Clock functions
def setTime():
   global clock
   clock = True
   x = datetime.datetime.now()
   h = x.hour
   m = x.minute
   if h > 12:
      h -= 12
   elif h == 0:
      h += 12
   if h == 1:
         for i in range(3,36):
            pixels[i] = ((0,0,0))
            pixels.show()
   h=h*3
   m=round((m/60*36)+36)
   for i in range (h):
      pixels[i] = (255,255,255)
   for i in range(36,m):
      pixels[i] = (255,0,0)
   for i in range(m,72):
      pixels[i] = (255,112,60)
   pixels.show()

def timer():
   global duration
   clockOff(0)
   global running
   running = True
   cycle = duration/12
   second = cycle/36
   g = 0
   b = 0

   for i in range(1,13):
      if running:
         for x in range(36):
            if running:
               pixels[x+36] = (255,g,b)
               pixels.show()
               time.sleep(second)
            else:
               break
         h=i*3
         for h in range(h):
            pixels[h] = (255,255,255)
            pixels.show()
         if g == 0:
            g = 112
            b = 60
         else:
            g = 0
            b = 0
      else:
         break

   
   for z in range(3):
      if running:
         pixels.fill((255,255,255))
         pixels.show()
         time.sleep(0.5)
         pixels.fill((0,0,0))
         pixels.show()
         time.sleep(0.5)
      else:
         break
   

def goose_start():
   g = threading.Thread(target=goose)
   g.start()

def geese_start():
   g = threading.Thread(target=geese)
   g.start()

def timer_start():
   g = threading.Thread(target=timer)
   g.start()

port= 9001
sub_topic="clock"
def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   print("subscribed with qos",granted_qos, "\n")
   pass
def on_message(client, userdata, message):
    global duration
    global running
    m = str(message.payload.decode("utf-8"))
    print("message received  ", str(message.payload.decode("utf-8")))
    if m == "red":
       red()
    elif m == "green":
       green()
    elif m == "blue":
       blue()
    elif m == "orange":
       orange()
    elif m == "on":
       whiteOn()
    elif m == "t":
       timeOn()
    elif m == "soft":
       duration = 240
       geese_start()
    elif m == "hard":
       duration = 600
       geese_start()
    elif m == "timer":
       timer_start()
    elif m == "off":
       clockOff(0)

def on_publish(client,userdata,mid):   #create function for callback
   print("data published mid=",mid, "\n")
   pass
def on_disconnect(client, userdata, rc):
   print("client disconnected ok") 

client= paho.Client("client-socks",transport='websockets')       #create client object
client.on_subscribe = on_subscribe       #assign function to callback
client.on_publish = on_publish        #assign function to callback
client.on_message = on_message        #assign function to callback
client.on_disconnect = on_disconnect
print("connecting to broker ",broker,"on port ",port)
client.connect(broker,port)           #establish connection
client.loop_start()
print("subscribing to ",sub_topic)
client.subscribe(sub_topic)
time.sleep(3)
client.publish("clock","t")    #publish
time.sleep(2)

#client.disconnect()

#Keep the program running and print out the date time
while True:
   if clock:
      setTime()
   print(clock)
   time.sleep(30)
