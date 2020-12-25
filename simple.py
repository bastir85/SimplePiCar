import smbus
import time
import RPi.GPIO as GPIO
import math 


from pwm import PWM

pwm = PWM(1, 0x40, 60)


_LED0_ON_L          = 0x06
_LED0_ON_H          = 0x07
_LED0_OFF_L         = 0x08
_LED0_OFF_H         = 0x09

_MODE1              = 0x00
_MODE2              = 0x01
_PRESCALE           = 0xFE
_SLEEP              = 0x10

_ALLCALL            = 0x01
_INVRT              = 0x10
_OUTDRV             = 0x04

PWM_A = 4
PWM_B = 5

Motor_A = 17
Motor_B = 27




#bus = smbus.SMBus(bus_number)


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A, GPIO.OUT)
    GPIO.setup(Motor_B, GPIO.OUT)
    
    #forward
    GPIO.output(Motor_A, 1)
    GPIO.output(Motor_B, 1)

def setup_pwm():
    write(0, 0, 0)
    bus.write_byte_data(address, _MODE2, _OUTDRV)
    bus.write_byte_data(address, _MODE1, _ALLCALL)
    time.sleep(0.005)

    mode1 = bus.read_byte_data(address, _MODE1)
    mode1 = mode1 & ~_SLEEP
    bus.write_byte_data(address, _MODE1, mode1)
    time.sleep(0.005)
    set_pwm_frequency(60)


def setup():
    setup_gpio()
    #setup_pwm()

def set_pwm_frequency(frequency):
    prescale_value = 25000000.0
    prescale_value /= 4096.0
    prescale_value /= frequency
    prescale_value -= 1.0
    prescale = math.floor(prescale_value + 0.5)

    old_mode = bus.read_byte_data(address, _MODE1)
    new_mode = (old_mode & 0x7F) | 0x10

    bus.write_byte_data(address, _MODE1, new_mode)
    bus.write_byte_data(address, _PRESCALE, int(math.floor(prescale)))
    bus.write_byte_data(address, _MODE1, old_mode)
    time.sleep(0.005)
    bus.write_byte_data(address, _MODE1, old_mode | 0x80)

def write(channel, on, off):
    #bus.write_byte_data(address, _LED0_ON_L+4*channel, on)
    #bus.write_byte_data(address, _LED0_ON_H+4*channel, on >> 8)
    bus.write_byte_data(address, _LED0_OFF_L+4*channel, off)
    bus.write_byte_data(address, _LED0_OFF_H+4*channel, off >> 8)

def set_angle(angle):
    assert angle >= -40 and angle <= 45 

    SERVO_CHANNEL = 0
    MIN_PULSE_WIDTH = 600
    MAX_PULSE_WIDTH = 2400
    frequency = 60
    
    angle += 90 
    pulse_wide = 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH
    pulse_wide = angle / 180 * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) + MIN_PULSE_WIDTH
    val = int(float(pulse_wide) / 1000000 * frequency * 4096)
            
    pwm.set_off_value(SERVO_CHANNEL, val)

setup()

for angle in [45,0,-40]:
    print(angle)
    set_angle(angle)
    time.sleep(1)
set_angle(6)
dir = 1
GPIO.output(Motor_A, 0)
GPIO.output(Motor_B, 0)
pwm.set_off_value(PWM_A, 2500) #left
pwm.set_off_value(PWM_B, 2500) #right
assert False
try:
    while(1):
        pwm.set_off_value(PWM_A, 0) #left
        pwm.set_off_value(PWM_B, 0) #right
        GPIO.output(Motor_A, dir)
        GPIO.output(Motor_B, dir)
        pwm.set_off_value(PWM_A, 2500) #left
        pwm.set_off_value(PWM_B, 2500) #right
        time.sleep(2)
        dir = not dir
except KeyboardInterrupt:
    pass

pwm.set_off_value(PWM_A,  0)
pwm.set_off_value(PWM_B,  0)

GPIO.cleanup()

