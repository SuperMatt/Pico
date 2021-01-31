import array, time, random
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 12
MAX_BRIGHT = 32
THREE_FOUR = int(MAX_BRIGHT*3/4)
HALF = int(MAX_BRIGHT/2)
ONE_FOUR = int(MAX_BRIGHT/4)
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

colors = [
    (MAX_BRIGHT, 0, 0),
    (THREE_FOUR, ONE_FOUR, 0),
    (HALF, HALF, 0),
    (ONE_FOUR, THREE_FOUR, 0),
    (0, MAX_BRIGHT, 0),
    (0, THREE_FOUR, ONE_FOUR),
    (0, HALF, HALF),
    (0, ONE_FOUR, THREE_FOUR),
    (0, 0, MAX_BRIGHT),
    (ONE_FOUR, 0, THREE_FOUR),
    (HALF, 0, HALF),
    (THREE_FOUR, 0, ONE_FOUR)
]


# Create the StateMachine with the ws2812 progam, putputting on Pin(15)
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(15))

# Start the StateMachine, it will wait for datat on its FIFO
sm.active(1)

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

j = 0

while True:
    for i in range(NUM_LEDS):
        num = i + j
        if num >= 12:
            num = num - 12

        red = colors[i][0]
        red_b = red<<8
        green = colors[i][1]
        green_b = green<<16
        blue = colors[i][2]
        blue_b = blue
        ar[num] = green_b + red_b + blue_b

    sm.put(ar, 8)

    j+=1
    if j > 11:
        j = 0
    time.sleep_ms(TWINKLE_TIME)
