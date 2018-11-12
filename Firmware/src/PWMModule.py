# -*- coding: utf-8 -*-
# Author: Cyrill Lippuner
# Date: October 2018
"""
SoftWEAR PWM module.

Adds PWM features and hardware commands capabilities
"""

from Config import PIN_MAP                                      # SoftWEAR Config module.
from MuxModule import Mux                                       # SoftWEAR MUX module.

from drivers.PWM_BASIC import PWMBasic                          # Driver module for basic input

# TODO: Special drivers for pwms (like PRU-driven)

# Create a MUX shadow instance as there is only one Mux
MuxShadow = Mux()

# List of all possible drivers
DRIVERS = [PWMBasic]

class PWM:
    """Implements basic pwm functionality."""

    # List of all connected drivers
    _connectedDrivers = []

    # List of connected devices dictionary.
    connectedDevices = []

    def __init__(self):
        """
        Class constructor.

            Initialises the module with the hardware options. This includes the scan pins and the possible MUX objects.
        """
        for pinConfig in PIN_MAP["PWM"]:                        # Loop all available pin configs
            pass



    def scan(self):
        """Update the connected devices dictionary list."""
        lastConnectedDrivers = self._connectedDrivers[:]        # Keep last connected driver list
        connectedDrivers = []                                   # New connected driver list
        connectedDevices = []                                   # New connected devices list
        disconnectedDriver = []                                 # Disconnected drivers

        for pinConfig in PIN_MAP["PWM"]:                        # Loop all available pin configs
            pin = pinConfig["DATA"]                             # DATA pin

            for lastDrv in lastConnectedDrivers:                # Test last connected drivers
                                                                # Check if drv already loaded and still connected
                if not lastDrv.getDeviceConnected():            # Device is disconnected
                    disconnectedDriver.append(lastDrv)
                elif lastDrv.getPin() == pin:                   # Device is still connected
                    connectedDrivers.append(lastDrv)            # Add to connected driver list
                    connectedDevices.append({   'pin': pin,     # Add to connected device list
                                                'mux': None,
                                                'name': lastDrv.getName(),
                                                'about': lastDrv.getAbout(),
                                                'settings': lastDrv.getSettings(),
                                                'dir': lastDrv.getDir(),
                                                'dim': lastDrv.getDim(),
                                                'mode': lastDrv.getMode(),
                                                'frequency': lastDrv.getFrequency(),
                                                'dutyFrequency': lastDrv.getDutyFrequency(),
                                                'flags': lastDrv.getFlags(),
                                                'val': 0,
                                                'vals': [],
                                                'cycle': 0})
                    break                                       # Break to next device
            else:                                               # Try new drivers if no existing was found
                for DRIVER in DRIVERS:                          # Test all drivers
                    drv = DRIVER(pin)                           # Test the different drivers
                    if not drv.getDeviceConnected():            # Validate driver connected
                        continue                                # Try next driver until none is left
                    drv.configureDevice()                       # Configure device
                    connectedDrivers.append(drv)                # Add to connected driver list
                    connectedDevices.append({   'pin': pin,     # Add to connected device list
                                                'mux': None,
                                                'name': drv.getName(),
                                                'about': drv.getAbout(),
                                                'settings': drv.getSettings(),
                                                'dir': drv.getDir(),
                                                'dim': drv.getDim(),
                                                'mode': drv.getMode(),
                                                'frequency': drv.getFrequency(),
                                                'dutyFrequency': drv.getDutyFrequency(),
                                                'flags': drv.getFlags(),
                                                'val':  0,
                                                'vals': [],
                                                'cycle': 0})
                    break                                       # Break to next device
                else:
                    pass                                        # No suitable driver has been found
        for drv in disconnectedDriver:                          # Clean up disconnected drivers
            drv.cleanup()
        self._connectedDrivers = connectedDrivers
        self.connectedDevices = connectedDevices


    def getValues(self):
        """Get values of a device."""
        for device in self.connectedDevices:                    # Loop all connected devices
            for drv in self._connectedDrivers:                  # Loop all connected drivers
                if device['name'] == drv.getName():             # Match for drv and device
                    values = drv.getValues()                    # Get last values from device and clear them
                    cycleDuration = drv.getCycleDuration()      # Get cycle duration for driver
                    if len(values) > 0:                         # Check if new data is available
                        device['val'] = values[-1][1]           # Get most recent value
                        device['vals'] = values                 # Get all new values
                        device['cycle'] = cycleDuration         # Get cycle duration


    def setValue(self, name, dim, value):
        """Set value for dim of a device."""
        for drv in self._connectedDrivers:                      # Check for driver
            if (drv.getName() == name):                         # If driver exists, set the value
                drv.setValue(dim, value)
                break

    def settings(self, settingsMessage):
        """Change settings of a device."""
        drv = None
        for el in self._connectedDrivers:                       # Check for driver
            if (el.getName() == settingsMessage['name']):
                drv = el
                break
        else:
            return

        if ('mode' in settingsMessage):                         # Check for mode settings
            try:                                                # Try to set the mode
                drv.setMode(settingsMessage['mode'])
            except ValueError:
                raise ValueError                                # Pass on the value error

        if ('flag' in settingsMessage):                         # Check for flag settings
            try:                                                # Try to set the flag
                drv.setFlag(settingsMessage['flag'], settingsMessage['value'])
            except ValueError:
                raise ValueError                                # Pass on the value error

        if ('frequency' in settingsMessage):                    # Check for frequency settings
            try:                                                # Try to set the frequency
                drv.setFrequency(settingsMessage['frequency'])
            except ValueError:
                raise ValueError                                # Pass on the value error

        if ('frequency' in settingsMessage):                    # Check for frequency settings
            try:                                                # Try to set the frequency
                drv.setFrequency(settingsMessage['frequency'])
            except ValueError:
                raise ValueError                                # Pass on the value error

        if ('dutyFrequency' in settingsMessage):                # Check for dutyFrequency settings
            try:                                                # Try to set the duty frequency
                drv.setDutyFrequency(settingsMessage['dutyFrequency'])
            except ValueError:
                raise ValueError                                # Pass on the value error
