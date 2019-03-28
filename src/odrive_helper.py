import serial
from serial.serialutil import SerialException

import sys
import time 
import traceback
import logging

import odrive
from odrive.enums import *

default_data_logger = logging.getLogger(__name__)
default_data_logger.setLevel(logging.DEBUG)

class ODriveFailure(Exception):
    pass

class ODriveHelper(object):
    odrv = None
    encoder_cpr = 4096
    axis_0 = None
    axis_1 = None
    is_connected = False
    is_prerolled = False

    def __init__(self, data_logger=None):
        self.data_logger = data_logger if data_logger else default_data_logger
    
    def connect(self, port=None, axis_0=0, timeout=30):
        if self.odrv:
            self.data_logger.info("Connected. Disconnecting and Reconnecting")
        try:
            self.odrv = odrive.find_any(timeout=timeout, logger=self.data_logger)
            self.axes = (self.odrv.axis0, self.odrv.axis1)
        except:
            self.data_logger.error("No Odrive was found. Is power on? Is the connection good?")
            return False
        self.axis_0 = self.odrv.axis0 if axis_0 == 0 else self.odrv.axis1
        self.axis_1 = self.odrv.axis1 if axis_0 == 0 else self.odrv.axis0
        self.econder_cpr = self.odrv.axis0.encoder.config.econder_cpr
        self.connected = True
        self.data_logger.info("Connected to ODrive. Hardware v%d.%d-%d, firmware v%d.%d.%d%s" % (
                        self.odrv.hw_version_major, self.odrv.hw_version_minor, self.odrv.hw_version_variant,
                        self.odrv.fw_version_major, self.odrv.fw_version_minor, self.odrv.fw_version_revision,
                        "-dev" if self.odrv.fw_version_unreleased else ""
                        ))
        return True
    
    def disconnect(self):
        self.axis_0 = False
        self.axis_1 = None
        self.is_prerolled = False
        if not self.odrv:
            self.data_logger.error("Not Connected.")
            return False
        try:
            self.odrv.release()
        except:
            self.data_logger.error("Timer error in: "+traceback.format_exc())
            return False
        finally:
            self.odrv = None
        return True

    def __del__(self):
        self.disconnect()

