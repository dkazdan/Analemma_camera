"""
Practice controlling model servos
Several tutorials out there.
Involved one with graphic slider interfaces: https://www.circuitbasics.com/how-to-use-servos-on-the-raspberry-pi/

"""

import RPi.GPIO as GPIO
from time import sleep

# set up the GPIO mode as BOARD to reference the PINs and not the BCM pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) # GPIO17, pin 11

# Or equivalently:
# servoPIN = 17
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN, GPIO.OUT)

pwm=GPIO.PWM(11, 50) # fifty pulses/second on that pin
pwm.start(0)         # starting at duty cycle zero

# Left -90 deg is 5%, Neutral is 7.5%, and Right +90 deg is 10%
pwm.ChangeDutyCycle(5) # left -90 deg position
sleep(1)
pwm.ChangeDutyCycle(7.5) # neutral position
sleep(1)
pwm.ChangeDutyCycle(10) # right +90 deg position
sleep(1)

# clean up by stopping the PWM signal and running the cleanup function
pwm.stop()
GPIO.cleanup()

# Might be useful:
def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(11, True) # sdame as .start, .stop?
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(duty)