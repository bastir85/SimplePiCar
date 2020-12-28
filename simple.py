import smbus
import time
import RPi.GPIO as GPIO
import math 


from pwm import PWM


PWM_SERVO_STEERING = 0
PWM_SERVO_CAM_HORIZONTAL = 1
PWM_SERVO_CAM_VERTICAL = 2
PWM_MOTOR_LEFT = 4
PWM_MOTOR_RIGHT = 5

DIRECTION_MOTOR_A = 17
DIRECTION_MOTOR_B = 27

pwm = PWM(1, 0x40, 60)

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIRECTION_MOTOR_A, GPIO.OUT)
    GPIO.setup(DIRECTION_MOTOR_B, GPIO.OUT)
    
    #forward
    GPIO.output(DIRECTION_MOTOR_A, 1)
    GPIO.output(DIRECTION_MOTOR_B, 1)


def set_angle(angle, servo_channel):
    assert angle >= -90 and angle <= 90 
    #passert angle >= -40 and angle <= 45 

    MIN_PULSE_WIDTH = 600
    MAX_PULSE_WIDTH = 2400
    frequency = 60
    
    angle += 90 
    pulse_wide = 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH
    pulse_wide = angle / 180.0 * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) + MIN_PULSE_WIDTH
    val = int(float(pulse_wide) / 1000000 * frequency * 4096)
    #print(f"servo = {SERVO_CHANNEL} val={val}")
    pwm.set_off_value(servo_channel, val)

setup_gpio()

for angle in [45,0,-40,0]:
    print(angle)
    set_angle(angle, PWM_SERVO_STEERING)
    time.sleep(2)

print('VERTICAL CAM')
for angle in range(-40,91,10):
    print(angle)
    set_angle(angle, PWM_SERVO_CAM_VERTICAL)
    time.sleep(1)

set_angle(0.0, PWM_SERVO_CAM_VERTICAL)

print('HORIZONTAL CAM')
# -30, 90
for angle in range(-90,91,10):
    print(angle)
    set_angle(angle, PWM_SERVO_CAM_HORIZONTAL)
    time.sleep(1)
set_angle(0.0, PWM_SERVO_CAM_HORIZONTAL)

dir = 1
set_angle(6, PWM_SERVO_STEERING)

try:
    while(1):
        pwm.set_off_value(PWM_MOTOR_LEFT, 0) #left
        pwm.set_off_value(PWM_MOTOR_RIGHT, 0) #right
        time.sleep(1)
        GPIO.output(DIRECTION_MOTOR_A, dir)
        GPIO.output(DIRECTION_MOTOR_B, dir)
        pwm.set_off_value(PWM_MOTOR_LEFT, 2500) #left
        pwm.set_off_value(PWM_MOTOR_RIGHT, 2500) #right
        time.sleep(2)
        dir = not dir
except KeyboardInterrupt:
    pass


pwm.set_off_value(PWM_MOTOR_LEFT, 0) #left
pwm.set_off_value(PWM_MOTOR_RIGHT, 0) #right
GPIO.cleanup()

