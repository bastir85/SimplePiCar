import smbus
import time
import RPi.GPIO as GPIO
import math 


from pwm import PWM
PWM_A = 4
PWM_B = 5
Motor_A = 17
Motor_B = 27

pwm = PWM(1, 0x40, 60)

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A, GPIO.OUT)
    GPIO.setup(Motor_B, GPIO.OUT)
    
    #forward
    GPIO.output(Motor_A, 1)
    GPIO.output(Motor_B, 1)


def set_angle(angle):
    assert angle >= -40 and angle <= 45 

    SERVO_CHANNEL = 0
    MIN_PULSE_WIDTH = 600
    MAX_PULSE_WIDTH = 2400
    frequency = 60
    
    angle += 90 
    pulse_wide = 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH
    pulse_wide = angle / 180.0 * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) + MIN_PULSE_WIDTH
    val = int(float(pulse_wide) / 1000000 * frequency * 4096)
    #print(f"servo = {SERVO_CHANNEL} val={val}")
    pwm.set_off_value(SERVO_CHANNEL, val)

setup_gpio()

dir = 1
for angle in [45,0,-40,0]:
    print(angle)
    set_angle(angle)
    time.sleep(2)

set_angle(6)

try:
    while(1):
        pwm.set_off_value(PWM_A, 0) #left
        pwm.set_off_value(PWM_B, 0) #right
        time.sleep(1)
        GPIO.output(Motor_A, dir)
        GPIO.output(Motor_B, dir)
        pwm.set_off_value(PWM_A, 2500) #left
        pwm.set_off_value(PWM_B, 2500) #right
        time.sleep(2)
        dir = not dir
except KeyboardInterrupt:
    pass


pwm.set_off_value(PWM_A, 0) #left
pwm.set_off_value(PWM_B, 0) #right
GPIO.cleanup()

