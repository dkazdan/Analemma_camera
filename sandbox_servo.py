"""
Practice controlling model servos
Several tutorials out there.
https://www.instructables.com/Controlling-Servo-Motor-Sg90-With-Raspberry-Pi-4/
Involved one with graphic slider interfaces: https://www.circuitbasics.com/how-to-use-servos-on-the-raspberry-pi/

"""

import RPi.GPIO as GPIO
from time import sleep
# stop warnings
GPIO.setwarnings(False)

# set up the GPIO mode as BOARD to reference the PINs and not the BCM pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) # GPIO17, pin 11

# Or equivalently:
# servoPIN = 17
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN, GPIO.OUT)

pwm=GPIO.PWM(11, 50) # fifty pulses/second on that pin
print('set zero angle')
pwm.start(0)         # starting at duty cycle zero
sleep(2)

def test_servo():
    # Left -60 deg is 2%, Neutral is 6%, and Right +60 deg is 10%
    print('left')
    pwm.ChangeDutyCycle(2) # left -90 deg position
    sleep(1)
    print('centered')
    pwm.ChangeDutyCycle(6) # neutral position
    sleep(1)
    print('right')
    pwm.ChangeDutyCycle(10) # right +90 deg position
    sleep(1)

    # clean up by stopping the PWM signal and running the cleanup function
    pwm.stop()
    GPIO.cleanup()

# Might be useful: TODO: Change this to match above numbers.
def setAngle(angle):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT) # GPIO17, pin 11
    duty = (angle / 18) + 2
    GPIO.output(11, True) # sdame as .start, .stop?
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(0)
    
if __name__ == '__main__':
    test_servo()
    sleep(1)
    print('set to 45 degrees')
    setAngle(45)
    print('\nend')