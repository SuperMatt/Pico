import machine
import utime

SLEEP=0.5

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_green = machine.Pin(15, machine.Pin.OUT)
led_red = machine.Pin(0, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN)

#status = [[1, 0, 0],[0, 1, 0],[0, 0, 1],[1,1,0],[1,0,1],[0,1,1]]
status = [[1, 0, 0],[0, 1, 0],[0, 0, 1]]

i = 0
while True:
    if button.value() == 1:
        led_red.value(status[i][0])
        led_green.value(status[i][1])
        led_onboard.value(status[i][2])
        i+=1
        if i >= len(status):
            i = 0
        utime.sleep(SLEEP)
#    else:
#        led_red.value(0)
#        led_green.value(0)
#        led_onboard.value(0)