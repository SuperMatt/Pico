
import array, time, random
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 12
MAX_BRIGHT = 4
THREE_FOUR = int(MAX_BRIGHT*3/4)
HALF = int(MAX_BRIGHT/2)
ONE_FOUR = int(MAX_BRIGHT/4)
TWINKLE_TIME = 100
BUTTON_MIN_TIME = 500
BUTTON_MIN_COUNT = int(BUTTON_MIN_TIME/TWINKLE_TIME)

def random_color():
    red = random.randrange(0, MAX_BRIGHT, 1)
    red_b = red<<8
    green = random.randrange(0, MAX_BRIGHT, 1)
    green_b = green<<16
    blue = random.randrange(0, MAX_BRIGHT, 1)
    blue_b = blue
    color = green_b + red_b + blue_b

    return color

def change_mode(ar):
    red = MAX_BRIGHT<<8
    green = MAX_BRIGHT<<16
    blue = MAX_BRIGHT
    white =  green + red + blue
    blank = 0

    for j in range(2):
        for i in range(NUM_LEDS):
            ar[i] = white
        
        sm.put(ar, 8)
        time.sleep_ms(200)

        for i in range(NUM_LEDS):
            ar[i] = blank

        sm.put(ar, 8)
        time.sleep_ms(200)

def rainbow_spin(ar):

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

    if ar[0] == 0:
        for i in range(NUM_LEDS):
            red = colors[i][0]
            red_b = red<<8
            green = colors[i][1]
            green_b = green<<16
            blue = colors[i][2]
            blue_b = blue
            ar[i] = green_b + red_b + blue_b
    else:
        start_index = 0
        for i in range(NUM_LEDS):
            if ar[i] == 1024: #red
                start_index = i + 1
                if start_index < 0:
                    start_index = 11


        for i in range(NUM_LEDS):
            color_index = i - start_index
            if color_index >= len(colors):
                color_index = color_index - 12

            red = colors[color_index][0]
            red_b = red<<8
            green = colors[color_index][1]
            green_b = green<<16
            blue = colors[color_index][2]
            blue_b = blue
            ar[i] = green_b + red_b + blue_b

    sm.put(ar, 8)

def random_twinkle(ar):
    led = random.randrange(0, NUM_LEDS, 1)
    color = random_color()
    ar[led] = color
    sm.put(ar,8)


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


# Create the StateMachine with the ws2812 progam, putputting on Pin(15)
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(15))

# Start the StateMachine, it will wait for datat on its FIFO
sm.active(1)

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

button = machine.Pin(16, machine.Pin.IN)

MODE = 0

button_count = 0

modes = [
    random_twinkle,
    rainbow_spin,
]

while True:

    if button.value() == 1:
        if button_count > BUTTON_MIN_COUNT:
            if button.value() == 1:
                MODE += 1
                if MODE >= len(modes):
                    MODE = 0
                change_mode(ar)
        button_count += 1
    else: 
        button_count = 0

    modes[MODE](ar)
    
    if button.value() == 0:
        button_count = 0

    time.sleep_ms(int(TWINKLE_TIME/2))

    if button.value() == 0:
        button_count = 0

    time.sleep_ms(int(TWINKLE_TIME/2))
