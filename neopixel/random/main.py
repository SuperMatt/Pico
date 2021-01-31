import array, time, random
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 12
MAX_BRIGHT = 16
TWINKLE_TIME = 100

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)

def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x ,1)             .side(0)  [T3 - 1]
    jmp(not_x, "do_zero") .side(1)  [T1 - 1]
    jmp("bitloop")        .side(1)  [T2 - 1]
    label("do_zero")
    nop()                 .side(0)  [T2 - 1]

def random_color():
    red = random.randrange(0, MAX_BRIGHT, 1)
    red_b = red<<8
    green = random.randrange(0, MAX_BRIGHT, 1)
    green_b = green<<16
    blue = random.randrange(0, MAX_BRIGHT, 1)
    blue_b = blue
    color = green_b + red_b + blue_b

    return color

# Create the StateMachine with the ws2812 progam, putputting on Pin(15)
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(15))

# Start the StateMachine, it will wait for datat on its FIFO
sm.active(1)

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

#for j in range(0, 255):
#    for i in range(NUM_LEDS):
#        ar[i] = j
#
#    sm.put(ar,8)
#    time.sleep_ms(100)
#
#for j in range(0, 255):
#    for i in range(NUM_LEDS):
#        ar[i] = j<<16 + j<<8 + j
#    sm.put(ar,8)
#    time.sleep_ms(100)

for i in range(NUM_LEDS):
    color = random_color()
    ar[i] = color

sm.put(ar,8)

while True:
    led = random.randrange(0, NUM_LEDS, 1)
    color = random_color()
    ar[led] = color


    sm.put(ar,8)
    time.sleep_ms(TWINKLE_TIME)
