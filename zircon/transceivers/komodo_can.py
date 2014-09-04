"""

"""

from komodo_py import *

from zircon.transceivers.base import BaseTransceiver

import sys


class KomodoTransceiver(BaseTransceiver):

    MAX_PKT_SIZE = 8
    NUM_GPIOS = 8

    def __init__(self, channel):

        # A, B, or AB
        self.channel = channel

        if self.channel == 'A':
            self.port = 0
        elif self.channel == 'B':
            self.port = 1
        else:
            self.port = -1

        # ms
        self.timeout = 1000

        # Hz
        self.bitrate = 1000000

        # Komodo object
        self.km = None
        self.data = array('B', '\0' * self.MAX_PKT_SIZE)
        self.samplerate_khz = None
        self.target_power = KM_TARGET_POWER_OFF

    @staticmethod
    def timestamp_to_ns(stamp, samplerate_khz):
        return stamp * 1000 / (samplerate_khz/1000)

    @staticmethod
    def status_str(status):

        if status == KM_OK:
            return 'OK'
        if status & KM_READ_TIMEOUT:
            return 'TIMEOUT'
        if status & KM_READ_ERR_OVERFLOW:
            return 'OVERFLOW'
        if status & KM_READ_END_OF_CAPTURE:
            return 'END OF CAPTURE'
        if status & KM_READ_CAN_ARB_LOST:
            return 'ARBITRATION LOST'
        if status & KM_READ_CAN_ERR:
            return 'ERROR %x' % (status & KM_READ_CAN_ERR_FULL_MASK)

    @staticmethod
    def events_str(events, bitrate):

        if events == 0:
            return ''
        if events & KM_EVENT_DIGITAL_INPUT:
            return 'GPIO CHANGE 0x%x;' % (events & KM_EVENT_DIGITAL_INPUT_MASK),
        if events & KM_EVENT_CAN_BUS_STATE_LISTEN_ONLY:
            return 'BUS STATE LISTEN ONLY;'
        if events & KM_EVENT_CAN_BUS_STATE_CONTROL:
            return 'BUS STATE CONTROL;'
        if events & KM_EVENT_CAN_BUS_STATE_WARNING:
            return 'BUS STATE WARNING;'
        if events & KM_EVENT_CAN_BUS_STATE_ACTIVE:
            return 'BUS STATE ACTIVE;'
        if events & KM_EVENT_CAN_BUS_STATE_PASSIVE:
            return 'BUS STATE PASSIVE;'
        if events & KM_EVENT_CAN_BUS_STATE_OFF:
            return 'BUS STATE OFF;'
        if events & KM_EVENT_CAN_BUS_BITRATE:
            return 'BITRATE %d kHz;' % (bitrate/1000)

    def open(self):

        # Open the interface
        self.km = km_open(self.port)

        if self.km <= 0:
            print('Unable to open Komodo on channel {}'.format(self.channel))
            print('Error code = {}'.format(self.km))
            return False

        # Acquire features.  Acquiring KM_FEATURE_CAN_A_CONTROL causes the
        # Komodo interface to ACK all packets transmitted on the bus. Remove
        # this feature to prevent the device from transmitting anything on
        # the bus.
        if self.port == KM_CAN_CH_A:
            ret = km_acquire(self.km,
                             KM_FEATURE_CAN_A_CONFIG |
                             KM_FEATURE_CAN_A_LISTEN |
                             # KM_FEATURE_CAN_A_CONTROL |
                             KM_FEATURE_GPIO_CONFIG |
                             KM_FEATURE_GPIO_LISTEN
                             )
        elif self.port == KM_CAN_CH_B:
            ret = km_acquire(self.km,
                             KM_FEATURE_CAN_B_CONFIG |
                             KM_FEATURE_CAN_B_LISTEN |
                             # KM_FEATURE_CAN_B_CONTROL |
                             KM_FEATURE_GPIO_CONFIG |
                             KM_FEATURE_GPIO_LISTEN
                             )
        else:
            print('ERROR unknown port: {}'.format(self.port))
            return False

        print 'Acquired features 0x%x' % ret

        # Set bitrate
        ret = km_can_bitrate(self.km, self.port, self.bitrate)
        print 'Bitrate set to %d kHz' % (ret/1000)

        # Set timeout
        km_timeout(self.km, self.timeout)
        print 'Timeout set to %d ms' % self.timeout

        # Set target power
        km_can_target_power(self.km, self.port, self.target_power)
        print 'Target power %s' % ('ON' if self.target_power else 'OFF')

        # Configure all GPIO pins as inputs
        for i in range(self.NUM_GPIOS):
            km_gpio_config_in(self.km, i, KM_PIN_BIAS_PULLUP,
                              KM_PIN_TRIGGER_BOTH_EDGES)
        print 'All pins set as inputs'
        print('')

        # Get samplerate
        self.samplerate_khz = km_get_samplerate(self.km)/1000

        # Enable Komodo
        ret = km_enable(self.km)
        if ret != KM_OK:
            print 'Unable to enable Komodo'
            return False

        return True

    def close(self):

        km_close(self.km)
        return True

    def read(self):

        ret, info, pkt, data = km_can_read(self.km, self.data)

        if ret == KM_COMMUNICATION_ERROR:
            print('[ERROR] Lost connection to Komodo! Exiting.')
            sys.exit(1)

        if ret < 0:
            print('[ERROR] {}'.format(ret))
            return None

        timestamp = self.timestamp_to_ns(info.timestamp, self.samplerate_khz)

        if info.status != KM_OK:
            print('[{}] ERROR: {}'.format(
                timestamp,
                self.status_str(info.status)
            ))
            return None

        if info.events:
            print('[{}] EVENT: {}'.format(
                timestamp,
                self.events_str(info.events, info.bitrate_hz)
            ))
            return None

        # If packet contained data, print it
        if pkt.remote_req:
            print('[{}] ID: {:x}, Remote request (rtr)'.format(
                timestamp,
                pkt.id
            ))
            return None

        # # Print the data message
        # print('[{}] ID: {:08X}, Data: {}'.format(
        #     timestamp,
        #     pkt.id,
        #     ' '.join(['{:02X}'.format(b) for b in data[:ret].tolist()])
        # ))

        return timestamp, pkt.id, data[:ret].tostring()

    def write(self, data):
        # TODO implement for sending commands
        raise NotImplementedError()
