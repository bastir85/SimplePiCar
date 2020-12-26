import smbus
import time
import math


class PWM:
    def __init__(self, bus_number, address, frequency):
        self.bus = smbus.SMBus(bus_number)
        self.address=address
        self._setup_chip(frequency)


    def _setup_chip(self, frequency):
        _MODE1              = 0x00
        _MODE2              = 0x01
        _PRESCALE           = 0xFE
        _SLEEP              = 0x10
        _ALLCALL            = 0x01
        _OUTDRV             = 0x04

        self.set_off_value(0, 0)
        self.write(_MODE2, _OUTDRV)
        self.write(_MODE1, _ALLCALL)
        time.sleep(0.005)

        mode1 = self.bus.read_byte_data(self.address, _MODE1)
        mode1 = mode1 & ~_SLEEP
        self.write( _MODE1, mode1)
        time.sleep(0.005)

        # Setup frequency
        prescale_value = 25000000.0
        prescale_value /= 4096.0
        prescale_value /= frequency
        prescale_value -= 1.0
        prescale = math.floor(prescale_value + 0.5)

        old_mode = self.bus.read_byte_data(self.address, _MODE1)
        new_mode = (old_mode & 0x7F) | 0x10

        self.write(_MODE1, new_mode)
        self.write(_PRESCALE, int(math.floor(prescale)))
        self.write(_MODE1, old_mode)
        time.sleep(0.005)
        self.write(_MODE1, old_mode | 0x80)


    def write(self, register, value):
        self.bus.write_byte_data(self.address, register, value)


    def set_off_value(self, channel, value):
        '''
            channel: led number
            value: 16 bit pcm value
        '''
        _LED0_OFF_L         = 0x08
        _LED0_OFF_H         = 0x09
        
        self.write(_LED0_OFF_L+4*channel, value)
        self.write(_LED0_OFF_H+4*channel, value >> 8)


    def set_on_value(self, channel, value):
        '''
            channel: led number
            value: 16 bit pcm value
        '''
        _LED0_ON_L          = 0x06
        _LED0_ON_H          = 0x07
     
        self.write(_LED0_ON_L+4*channel, value)
        self.write(_LED0_ON_H+4*channel, value >> 8)

