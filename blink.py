import time
import board
import neopixel
#from adafruit_led_animation.animation.blink import Blink

pin = board.D18
pix = 300

pixels = neopixel.NeoPixel(pin, pix, brightness=1, auto_write=False)

speed = 0.2

pixels.fill((255,0,0))
pixels.show()
time.sleep(speed)
pixels.fill((0,255,0))
pixels.show()
time.sleep(speed)
pixels.fill((0,0,255))
pixels.show()
time.sleep(speed)
pixels.fill((0,0,0))
pixels.show()


