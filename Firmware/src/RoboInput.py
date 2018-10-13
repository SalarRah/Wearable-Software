# -*- coding: utf-8 -*-
"""
SoftWEAR Input module.

Adds Input features and hardware detection
capabilities of the underlying mraa library.
"""

import RoboMUX as mux                                           # SoftWEAR MUX class.

from INPUT_BASIC import Input                                   # SoftWEAR MUX class.

# Translation between normal ADC indexes and the ones that mraa uses
idx2mraa = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7}

# Translation between string IDs and normal ADC indexes (to be translated to MRAA)
str2idx = {'P9_39': 0, 'P9_40': 1, 'P9_37': 2, 'P9_38': 3, 'P9_33': 4, 'P9_36': 5, 'P9_35': 6}

ASSIGNED_PINS = [
    "P8_14",
    "P8_41",
    "P8_42",
    "P8_43",
    "P8_44"
]
ASSIGNED_MUX_PINS = [
#    A        B        C        Detect
    ["P8_41", "P8_42", "P8_43", "P8_44"]
]

# TODO: Check if pins are free

# TODO: Special drivers for basic inputs


class RoboInput:
    """Implements basic input functionality."""

    # List of scan pins to be initialized – SHOULD BE CONSTAT THROUGHT EXECUTION.
    # SCAN_PINS = [0, 1, 2]

    # Set here the MUX pins for each scan pin. Mux pins are(in order): A, B, C, detect
    # SCAN_PINS_MUX = [None, ["P8_41", "P8_42", "P8_43", "P8_44"], None]

    # List of all initialized pins. Created from the list of scan pins.
    _connectedPinLists = []

    # List of connected drivers
    _connectedDrivers = []

    # List of all drivers
    _drivers = []

    # List of connected devices dictionary. Contains: {chn, subchn, val, cnt, actv}. Subchannel is -1 in case no MUX is connected.
    connectedDevices = []

    # List of all devices dictionary. Contains: {chn, val, cnt, actv, sublist}. Val is -1 for MUXed channels. Sublist is a list of dictionaries for all MUXed values: {subchn, val, cnt, actv}
    devices = []

    def __init__(self):
        """
        Class constructor.

            Initialises the module with the hardware options. This includes the scan pins and the possible MUX objects.
        """
        for pin in ASSIGNED_PINS:                               # Loop all available pins
                                                                # Check if pin is used as MUX or else
            if pin in [item for sublist in ASSIGNED_MUX_PINS for item in sublist]:
                pass
            else:
                drv = Input(pin)                                # Init as input device
                drv.configureDevice()                           # Configure device
                self._drivers.append(drv)                       # Add to driver list
                self._connectedDrivers.append(drv)              # Add to connected driver list
                self.devices.append({   'chn': pin,             # Add to device list
                                        'subchn': -1,
                                        'device': '{}@Input[{}]'.format(drv.getDevice(), pin),
                                        'dir': drv.dir(),
                                        'dim': drv.dim(),
                                        'vals': []})
                self.connectedDevices.append({   'chn': pin,    # Add to connected device list
                                        'subchn': -1,
                                        'device': '{}@Input[{}]'.format(drv.getDevice(), pin),
                                        'dir': drv.dir(),
                                        'dim': drv.dim(),
                                        'vals': []})

        # self._pin_objects = []              # Initialise the mraa pin object list
        # self._mux_object = mux.RoboMUX()    # Create the SoftWEAR Mux object for the ADC
        # for pin in self.SCAN_PINS:              # Go through all configured ADC pins
        #     # Validate the pin and get the mraa index associated with it.
        #     scan_idx, mraa_idx = self.validate_pin(pin)
        #
        #     # Test for any configuration error
        #     if scan_idx is -1 or mraa_idx is -1:
        #         raise ValueError("Init Error: pin scan list is incorrect!")
        #
        #     x = mraa.Aio(mraa_idx)          # Create the mraa object for the pin
        #     self._pin_objects.append(x)     # Append the mraa object to the list
        #
        #     if self.SCAN_PINS_MUX[scan_idx] is not None:
        #         # If we have a MUX configuration for this pin, add it to the MUX list
        #         self._mux_object.add_mux_slot('ADC', pin, self.SCAN_PINS_MUX[scan_idx][:3], self.SCAN_PINS_MUX[scan_idx][-1])
        #
        #     # Create a corresponding output dictionary and add it to the all_devices list
        #     self.all_devices.append({'chn':pin, 'val':0, 'cnt':0, 'actv':False, 'sublist':[]})


    # def validate_pin(self, pin):
    #     """ Returns scan_idx, mraa_idx if succesful, -1, -1 if not.
    #         The scan_idx is the pin index in the class scan list.
    #         The mraa_idx is the pin number used by the mraa library. """
    #     idx = None
    #     try:    # Parse the input parameter
    #         if isinstance(pin, str):
    #             idx = str2idx[pin]  # Pin is in string format -> use dict
    #     except KeyError:            # Key error means it's not in str2idx dict.
    #         return -1, -1
    #
    #     if not idx and isinstance(pin, int):
    #         idx = pin               # If pin is already a number, save it
    #
    #     if idx is None:             # If we don't have a index by now -> error
    #         return -1, -1
    #
    #     try:
    #         mraa_idx = idx2mraa[idx]    # Convert index to mraa index
    #     except KeyError:                # Key error -> pin is not mraa ADC pin
    #         return -1, -1
    #
    #     try:                # Get the scan index from the class scan list
    #         scan_idx = self.SCAN_PINS.index(idx)
    #     except ValueError:  # Value Error -> pin not in class scan list
    #         return -1, mraa_idx
    #
    #     return scan_idx, mraa_idx

    def validatePin(self, pin):
        """Check the pin if listed and connected."""
        return pin in ASSIGNED_PINS                             # Look for pin to be assigned

    def getValues(self, pin):
        """
        Get the Voltage value reading of the specified channel pin.

            Only works on the class list of initialized pins.
        """
        if self.validatePin(pin):                               # Given pin is not a valid input pin
            raise ValueError("Parameter error: pin is invalid - pin should either be a number 0-6 or a string(e.g. P9_39)")
        else:
            for drv in self._drivers:
                if drv.pin() == pin:
                    return drv.getValues()                      # Get values from driver
            else:
                raise ValueError("Parameter error: driver not found")


    # def get_all_mv(self):
    #     """ Gets the Voltage value reading of all the configured ADC channel pins.
    #         Returns a list of voltage values corresponding to the scan list.
    #         If any mux is connected, a list will be returned instead of a value in
    #         the corresponding channel slot (e.g. [1, 2, [3, 3, 3, ... 3]])"""
    #     ret = []                    # Init return object to an epty list
    #     for pin in self.SCAN_PINS:  # Go through all pins in the ADC scan list
    #         # Append the MUXed values to the return object. This is either one
    #         # value (no MUX connected), or a list of values (MUX connected)
    #         ret.append(self._mux_object.get_muxed_values(pin, self.get_mv, pin))
    #     return ret                  # Return the return object

    def updateValues(self):
        """Update the values of the devices."""
        for drv in self._connectedDrivers:                      # Loop all drivers
            for device in self.connectedDevices:                # Loop all devices
                if device.device == '{}@Input[{}]'.format(drv.getDevice(), drv.pin()): # Match for drv and device
                    device.values = drv.getValues()             # Update values

        # Get the channel index corresponding to the current channel element
        # chn_idx = next((index for (index, d) in enumerate(self.all_devices) if d["chn"] == chn))
        # c_dict = self.all_devices[chn_idx]  # Select the current element dictionary
        # ret_list = []                       # Initialize the return object to an empty list
        #
        # if isinstance(val, list):           # Check if we are dealing with a MUXed value or not
        #     c_dict['val'] = -1              # Since val is a list -> we will use the 'sublist'
        #     c_dict['actv'] = False          # Reset the 'actv' value
        #     mux_con_flag = False            # Goes 'True' if this is the iteration which detected the MUX
        #     for val_idx, val_mv in enumerate(val):
        #         try:    # Try and get the dictionary of the MUXed value index
        #             sbchn_idx = next((index for (index, d) in enumerate(c_dict['sublist']) if d["subchn"] == val_idx))
        #             sbchn_dict = c_dict['sublist'][sbchn_idx] # Get the subchannel dictionanry
        #             sbchn_dict['val'] = val_mv          # Set the subchannel voltage value to the measured one
        #             if val_mv <= 0.005 and sbchn_dict['cnt'] > 0:
        #                 sbchn_dict['cnt'] -= 1          # Decrease counter value if new voltage is almost 0
        #                 if sbchn_dict['cnt'] == 0 and sbchn_dict['actv']:
        #                     sbchn_dict['actv'] = False  # Disable channel if the counter reached 0
        #                     # Add disconnected event to return list
        #                     ret_list.append({'chn':chn, 'subchn':sbchn_idx, 'event':'disc', 'mux':'none'})
        #             elif val_mv >= 0.005 and sbchn_dict['cnt'] < self.timeout_ticks:
        #                 sbchn_dict['cnt'] += 1          # Increment counter value if new voltage is not 0
        #                 if sbchn_dict['cnt'] == self.timeout_ticks and sbchn_dict['actv'] == False:
        #                     sbchn_dict['actv'] = True   # Enable channel if the counter reached the threshold
        #                     # Add connected event to return list
        #                     ret_list.append({'chn':chn, 'subchn':sbchn_idx, 'event':'conn', 'mux':'none'})
        #             if sbchn_dict['actv'] == True:      # For any active subchannel, the channel is active
        #                 c_dict['actv'] = True
        #         except: # We don't have a dictionary for the MUXed value yet -> add a default one
        #             c_dict['sublist'].append({'chn':chn, 'subchn':val_idx, 'val':val_mv, 'cnt':1, 'actv':False})
        #             mux_con_flag = True                 # Mux connected event detected!
        #     if mux_con_flag:    # Return MUX connected event. Used flag to avoid multiple instances of same event
        #         ret_list.append({'chn':chn, 'subchn':-1, 'event':'none', 'mux':'conn'})
        # else:   # We are NOT dealing with a MUXed value -> No mux connected
        #     if len(c_dict['sublist']) > 0: # Return MUX disconnected event
        #         ret_list.append({'chn':chn, 'subchn':-1, 'event':'none', 'mux':'disc'})
        #     c_dict['sublist'] = []  # Since no MUX connected -> we have no sublist
        #     c_dict['val'] = val     # Since val is a value -> update it
        #
        #     if val <= 0.005 and c_dict['cnt'] > 0:     # Reading of 0 on an existing channel with cnt > 0
        #         c_dict['cnt'] -= 1          # Decrease counter value
        #         if c_dict['cnt'] == 0 and c_dict['actv']:
        #             c_dict['actv'] = False  # Disable channel if the counter reached 0
        #             ret_list.append({'chn':chn, 'subchn':-1, 'event':'disc', 'mux':'none'})
        #     elif val >= 0.005 and c_dict['cnt'] < self.timeout_ticks:
        #         c_dict['cnt'] += 1          # Increment counter value
        #         if c_dict['cnt'] == self.timeout_ticks and c_dict['actv'] == False:
        #             c_dict['actv'] = True  # Enable channel if the counter reached the threshold
        #             ret_list.append({'chn':chn, 'subchn':-1, 'event':'conn', 'mux':'none'})
        # return ret_list


    def update(self):
        """
        Update the connected devices dictionary list.

            Returns a new list of dictionaries on the form of {'chn', 'subchn', 'event':'disc'/'conn'/'none', 'mux':'disc'/'conn'/'none'}
        """
        self.updateValues()                                     # Update values for all devices
        return self.connectedDevices                            # Return the connected devices
