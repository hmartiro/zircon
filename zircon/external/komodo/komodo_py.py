#==========================================================================
# Komodo Interface Library
#--------------------------------------------------------------------------
# Copyright (c) 2011 Total Phase, Inc.
# All rights reserved.
# www.totalphase.com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# - Neither the name of Total Phase, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#--------------------------------------------------------------------------
# To access Komodo devices through the API:
#
# 1) Use one of the following shared objects:
#      komodo.so      --  Linux shared object
#      komodo.dll     --  Windows dynamic link library
#
# 2) Along with one of the following language modules:
#      komodo.c/h     --  C/C++ API header file and interface module
#      komodo_py.py   --  Python API
#      komodo.bas     --  Visual Basic 6 API
#      komodo.cs      --  C# .NET source
#      komodo_net.dll --  Compiled .NET binding
#==========================================================================


#==========================================================================
# VERSION
#==========================================================================
KM_API_VERSION    = 0x010a   # v1.10
KM_REQ_SW_VERSION = 0x010a   # v1.10

import os
import sys
try:
    import komodo as api
except ImportError, ex1:
    import imp, platform
    ext = platform.system() in ('Windows', 'Microsoft') and '.dll' or '.so'
    try:
        api = imp.load_dynamic('komodo', 'komodo' + ext)
    except ImportError, ex2:
        import_err_msg  = 'Error importing komodo%s\n' % ext
        import_err_msg += '  Architecture of komodo%s may be wrong\n' % ext
        import_err_msg += '%s\n%s' % (ex1, ex2)
        raise ImportError(import_err_msg)

KM_SW_VERSION      = api.py_version() & 0xffff
KM_REQ_API_VERSION = (api.py_version() >> 16) & 0xffff
KM_LIBRARY_LOADED  = \
    ((KM_SW_VERSION >= KM_REQ_SW_VERSION) and \
     (KM_API_VERSION >= KM_REQ_API_VERSION))

from array import array, ArrayType
import struct


#==========================================================================
# HELPER FUNCTIONS
#==========================================================================
def array_u08 (n):  return array('B', '\0'*n)
def array_u16 (n):  return array('H', '\0\0'*n)
def array_u32 (n):  return array('I', '\0\0\0\0'*n)
def array_u64 (n):  return array('K', '\0\0\0\0\0\0\0\0'*n)
def array_s08 (n):  return array('b', '\0'*n)
def array_s16 (n):  return array('h', '\0\0'*n)
def array_s32 (n):  return array('i', '\0\0\0\0'*n)
def array_s64 (n):  return array('L', '\0\0\0\0\0\0\0\0'*n)
def array_f32 (n):  return array('f', '\0\0\0\0'*n)
def array_f64 (n):  return array('d', '\0\0\0\0\0\0\0\0'*n)


#==========================================================================
# STATUS CODES
#==========================================================================
# All API functions return an integer which is the result of the
# transaction, or a status code if negative.  The status codes are
# defined as follows:
# enum km_status_t
# General codes (0 to -99)
KM_OK                      =    0
KM_UNABLE_TO_LOAD_LIBRARY  =   -1
KM_UNABLE_TO_LOAD_DRIVER   =   -2
KM_UNABLE_TO_LOAD_FUNCTION =   -3
KM_INCOMPATIBLE_LIBRARY    =   -4
KM_INCOMPATIBLE_DEVICE     =   -5
KM_COMMUNICATION_ERROR     =   -6
KM_UNABLE_TO_OPEN          =   -7
KM_UNABLE_TO_CLOSE         =   -8
KM_INVALID_HANDLE          =   -9
KM_CONFIG_ERROR            =  -10
KM_PARAM_ERROR             =  -11
KM_FUNCTION_NOT_AVAILABLE  =  -12
KM_FEATURE_NOT_ACQUIRED    =  -13
KM_NOT_DISABLED            =  -14
KM_NOT_ENABLED             =  -15

# CAN codes (-100 to -199)
KM_CAN_READ_EMPTY          = -101
KM_CAN_SEND_TIMEOUT        = -102
KM_CAN_SEND_FAIL           = -103
KM_CAN_ASYNC_EMPTY         = -104
KM_CAN_ASYNC_MAX_REACHED   = -105
KM_CAN_ASYNC_PENDING       = -106
KM_CAN_ASYNC_TIMEOUT       = -107
KM_CAN_AUTO_BITRATE_FAIL   = -108


#==========================================================================
# GENERAL TYPE DEFINITIONS
#==========================================================================
# Komodo handle type definition
# typedef Komodo => integer

# Komodo version matrix.
#
# This matrix describes the various version dependencies
# of Komodo components.  It can be used to determine
# which component caused an incompatibility error.
#
# All version numbers are of the format:
#   (major << 8) | minor
#
# ex. v1.20 would be encoded as:  0x0114
class KomodoVersion:
    def __init__ (self):
        # Software, firmware, and hardware versions.
        self.software       = 0
        self.firmware       = 0
        self.hardware       = 0

        # Firmware revisions that are compatible with this software version.
        # The top 16 bits gives the maximum accepted fw revision.
        # The lower 16 bits gives the minimum accepted fw revision.
        self.fw_revs_for_sw = 0

        # Hardware revisions that are compatible with this software version.
        # The top 16 bits gives the maximum accepted hw revision.
        # The lower 16 bits gives the minimum accepted hw revision.
        self.hw_revs_for_sw = 0

        # Software requires that the API interface must be >= this version.
        self.api_req_by_sw  = 0

# Komodo feature set
#
# This bitmask field describes the features available on this device.
#
# When returned by km_features() or km_open_ext(), it refers to the
# potential features of the device.
# When used as a parameter by km_enable() or km_disable(), it refers
# to the features that the user wants to use.
# And when returned by km_disable(), it refers to the features currently
# in use by the user.
KM_FEATURE_GPIO_LISTEN = 0x00000001
KM_FEATURE_GPIO_CONTROL = 0x00000002
KM_FEATURE_GPIO_CONFIG = 0x00000004
KM_FEATURE_CAN_A_LISTEN = 0x00000008
KM_FEATURE_CAN_A_CONTROL = 0x00000010
KM_FEATURE_CAN_A_CONFIG = 0x00000020
KM_FEATURE_CAN_B_LISTEN = 0x00000040
KM_FEATURE_CAN_B_CONTROL = 0x00000080
KM_FEATURE_CAN_B_CONFIG = 0x00000100

#==========================================================================
# GENERAL API
#==========================================================================
# Get a list of ports to which Komodo devices are attached.
#
# nelem   = maximum number of elements to return
# devices = array into which the port numbers are returned
#
# Each element of the array is written with the port number.
# Devices that are in-use are ORed with KM_PORT_NOT_FREE (0x8000).
#
# ex.  devices are attached to ports 0, 1, 2
#      ports 0 and 2 are available, and port 1 is in-use.
#      array => 0x0000, 0x8001, 0x0002
#
# If the array is NULL, it is not filled with any values.
# If there are more devices than the array size, only the
# first nmemb port numbers will be written into the array.
#
# Returns the number of devices found, regardless of the
# array size.
KM_PORT_NOT_FREE = 0x8000
KM_PORT_NUM_MASK = 0x00ff
def km_find_devices (ports):
    """usage: (int return, u16[] ports) = km_find_devices(u16[] ports)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function.

    Additionally, for arrays that are filled by the API function, an
    integer can be passed in place of the array argument and the API
    will automatically create an array of that length.  All output
    arrays, whether passed in or generated, are passed back in the
    returned tuple."""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # ports pre-processing
    __ports = isinstance(ports, int)
    if __ports:
        (ports, num_ports) = (array_u16(ports), ports)
    else:
        (ports, num_ports) = isinstance(ports, ArrayType) and (ports, len(ports)) or (ports[0], min(len(ports[0]), int(ports[1])))
        if ports.typecode != 'H':
            raise TypeError("type for 'ports' must be array('H')")
    # Call API function
    (_ret_) = api.py_km_find_devices(num_ports, ports)
    # ports post-processing
    if __ports: del ports[max(0, min(_ret_, len(ports))):]
    return (_ret_, ports)


# Get a list of ports to which Komodo devices are attached.
#
# This function is the same as km_find_devices() except that
# it returns the unique IDs of each Komodo device.  The IDs
# are guaranteed to be non-zero if valid.
#
# The IDs are the unsigned integer representation of the 10-digit
# serial numbers.
def km_find_devices_ext (ports, unique_ids):
    """usage: (int return, u16[] ports, u32[] unique_ids) = km_find_devices_ext(u16[] ports, u32[] unique_ids)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function.

    Additionally, for arrays that are filled by the API function, an
    integer can be passed in place of the array argument and the API
    will automatically create an array of that length.  All output
    arrays, whether passed in or generated, are passed back in the
    returned tuple."""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # ports pre-processing
    __ports = isinstance(ports, int)
    if __ports:
        (ports, num_ports) = (array_u16(ports), ports)
    else:
        (ports, num_ports) = isinstance(ports, ArrayType) and (ports, len(ports)) or (ports[0], min(len(ports[0]), int(ports[1])))
        if ports.typecode != 'H':
            raise TypeError("type for 'ports' must be array('H')")
    # unique_ids pre-processing
    __unique_ids = isinstance(unique_ids, int)
    if __unique_ids:
        (unique_ids, num_ids) = (array_u32(unique_ids), unique_ids)
    else:
        (unique_ids, num_ids) = isinstance(unique_ids, ArrayType) and (unique_ids, len(unique_ids)) or (unique_ids[0], min(len(unique_ids[0]), int(unique_ids[1])))
        if unique_ids.typecode != 'I':
            raise TypeError("type for 'unique_ids' must be array('I')")
    # Call API function
    (_ret_) = api.py_km_find_devices_ext(num_ports, num_ids, ports, unique_ids)
    # ports post-processing
    if __ports: del ports[max(0, min(_ret_, len(ports))):]
    # unique_ids post-processing
    if __unique_ids: del unique_ids[max(0, min(_ret_, len(unique_ids))):]
    return (_ret_, ports, unique_ids)


# Open the Komodo port.
#
# The port number is a zero-indexed integer.
#
# The port number is the same as that obtained from the
# km_find_devices() function above.
#
# Returns an Komodo handle, which is guaranteed to be
# greater than zero if it is valid.
#
# This function is recommended for use in simple applications
# where extended information is not required.  For more complex
# applications, the use of km_open_ext() is recommended.
def km_open (port_number):
    """usage: Komodo return = km_open(int port_number)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_open(port_number)


# Open the Komodo port, returning extended information
# in the supplied structure.  Behavior is otherwise identical
# to km_open() above.  If 0 is passed as the pointer to the
# structure, this function is exactly equivalent to km_open().
#
# The structure is zeroed before the open is attempted.
# It is filled with whatever information is available.
#
# For example, if the firmware version is not filled, then
# the device could not be queried for its version number.
#
# The feature list is a bitmap of Komodo resources, with the same
# mapping as obtained from the km_features() function below.
# Details on the bitmask are found above.
#
# This function is recommended for use in complex applications
# where extended information is required.  For more simple
# applications, the use of km_open() is recommended.
class KomodoExt:
    def __init__ (self):
        # Version matrix
        self.version  = KomodoVersion()

        # Features of this device.
        self.features = 0

def km_open_ext (port_number):
    """usage: (Komodo return, KomodoExt km_ext) = km_open_ext(int port_number)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    (_ret_, c_km_ext) = api.py_km_open_ext(port_number)
    # km_ext post-processing
    km_ext = KomodoExt()
    (km_ext.version.software, km_ext.version.firmware, km_ext.version.hardware, km_ext.version.fw_revs_for_sw, km_ext.version.hw_revs_for_sw, km_ext.version.api_req_by_sw, km_ext.features) = c_km_ext
    return (_ret_, km_ext)


# Close the Komodo port.
def km_close (komodo):
    """usage: int return = km_close(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_close(komodo)


# Return the port for this Komodo handle.
#
# The port number is a zero-indexed integer identical to those
# returned by km_find_devices() above.  This includes the count of
# interfaces in use in the upper byte.
def km_port (komodo):
    """usage: int return = km_port(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_port(komodo)


# Return the device features as a bit-mask of values, or an error code
# if the handle is not valid.  Details on the bitmask are found above.
def km_features (komodo):
    """usage: int return = km_features(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_features(komodo)


# Return the unique ID for this Komodo adapter.
# IDs are guaranteed to be non-zero if valid.
# The ID is the unsigned integer representation of the
# 10-digit serial number.
def km_unique_id (komodo):
    """usage: u32 return = km_unique_id(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_unique_id(komodo)


# Return the status string for the given status code.
# If the code is not valid or the library function cannot
# be loaded, return a NULL string.
def km_status_string (status):
    """usage: str return = km_status_string(int status)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_status_string(status)


# Return the version matrix for the device attached to the
# given handle.  If the handle is 0 or invalid, only the
# software and required api versions are set.
def km_version (komodo):
    """usage: (int return, KomodoVersion version) = km_version(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    (_ret_, c_version) = api.py_km_version(komodo)
    # version post-processing
    version = KomodoVersion()
    (version.software, version.firmware, version.hardware, version.fw_revs_for_sw, version.hw_revs_for_sw, version.api_req_by_sw) = c_version
    return (_ret_, version)


# Sleep for the specified number of milliseconds.
# Accuracy depends on the operating system scheduler.
# Returns the number of milliseconds slept.
def km_sleep_ms (milliseconds):
    """usage: u32 return = km_sleep_ms(u32 milliseconds)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_sleep_ms(milliseconds)


# Acquire device features.
# Returns the features that are currently acquired.
def km_acquire (komodo, features):
    """usage: int return = km_acquire(Komodo komodo, u32 features)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_acquire(komodo, features)


# Release device features.
# Returns the features that are still acquired.
def km_release (komodo, features):
    """usage: int return = km_release(Komodo komodo, u32 features)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_release(komodo, features)



#==========================================================================
# CAN API
#==========================================================================
# These special timeout constants can be used with the functions
# km_timeout and km_can_async_collect.
KM_TIMEOUT_IMMEDIATE = 0
KM_TIMEOUT_INFINITE = -1
# Set the timeout of the km_can_read function to the specified
# number of milliseconds.
def km_timeout (komodo, timeout_ms):
    """usage: int return = km_timeout(Komodo komodo, u32 timeout_ms)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_timeout(komodo, timeout_ms)


# Standard enumeration for the CAN channels available on the Komodo.
# enum km_can_ch_t
KM_CAN_CH_A = 0
KM_CAN_CH_B = 1

# CAN Bus state constants.
KM_CAN_BUS_STATE_LISTEN_ONLY = 0x00000001
KM_CAN_BUS_STATE_CONTROL = 0x00000002
KM_CAN_BUS_STATE_WARNING = 0x00000004
KM_CAN_BUS_STATE_ACTIVE = 0x00000008
KM_CAN_BUS_STATE_PASSIVE = 0x00000010
KM_CAN_BUS_STATE_OFF = 0x00000020
# Retreive the current bus state of the supplied CAN channel
def km_can_query_bus_state (komodo, channel):
    """usage: (int return, u08 bus_state, u08 rx_error, u08 tx_error) = km_can_query_bus_state(Komodo komodo, km_can_ch_t channel)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_can_query_bus_state(komodo, channel)


# Set the capture latency to the specified number of milliseconds.
# This number determines the minimum time that a read call will
# block if there is no available data.  Lower times result in
# faster turnaround at the expense of reduced buffering.  Setting
# this parameter too low can cause packets to be dropped.
def km_latency (komodo, latency_ms):
    """usage: int return = km_latency(Komodo komodo, u32 latency_ms)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_latency(komodo, latency_ms)


# Config mask for km_can_configure
KM_CAN_CONFIG_NONE = 0x00000000
KM_CAN_CONFIG_LISTEN_SELF = 0x00000001
def km_can_configure (komodo, config):
    """usage: int return = km_can_configure(Komodo komodo, u32 config)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_can_configure(komodo, config)


# Set the bus timeout.  If a zero is passed as the timeout,
# the timeout is unchanged and the current timeout is returned.
def km_can_bus_timeout (komodo, channel, timeout_ms):
    """usage: int return = km_can_bus_timeout(Komodo komodo, km_can_ch_t channel, u16 timeout_ms)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_can_bus_timeout(komodo, channel, timeout_ms)


# Set the CAN bit rate in hertz on the given channel.  If a zero is
# passed as the bitrate, the bitrate is unchanged.  In all cases, the
# call will return the bitrate that will be in effect.
KM_KHZ = 1000
KM_MHZ = 1000000
def km_can_bitrate (komodo, channel, bitrate_hz):
    """usage: int return = km_can_bitrate(Komodo komodo, km_can_ch_t channel, u32 bitrate_hz)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_can_bitrate(komodo, channel, bitrate_hz)


def km_can_auto_bitrate (komodo, channel):
    """usage: int return = km_can_auto_bitrate(Komodo komodo, km_can_ch_t channel)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_can_auto_bitrate(komodo, channel)


def km_can_auto_bitrate_ext (komodo, channel, bitrates_hz):
    """usage: int return = km_can_auto_bitrate_ext(Komodo komodo, km_can_ch_t channel, u32[] bitrates_hz)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function."""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # bitrates_hz pre-processing
    (bitrates_hz, num_bitrates_hz) = isinstance(bitrates_hz, ArrayType) and (bitrates_hz, len(bitrates_hz)) or (bitrates_hz[0], min(len(bitrates_hz[0]), int(bitrates_hz[1])))
    if bitrates_hz.typecode != 'I':
        raise TypeError("type for 'bitrates_hz' must be array('I')")
    # Call API function
    return api.py_km_can_auto_bitrate_ext(komodo, channel, num_bitrates_hz, bitrates_hz)


# Get the sample rate in hertz.
def km_get_samplerate (komodo):
    """usage: int return = km_get_samplerate(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_get_samplerate(komodo)


# Configure the target power.  Returns power status or error code.
# enum km_power_t
KM_TARGET_POWER_QUERY = 0x02
KM_TARGET_POWER_OFF   = 0x00
KM_TARGET_POWER_ON    = 0x01

# Set the target power for the specified CAN channel.
def km_can_target_power (komodo, channel, power):
    """usage: int return = km_can_target_power(Komodo komodo, km_can_ch_t channel, km_power_t power)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_can_target_power(komodo, channel, power)


# Enable the Komodo.
def km_enable (komodo):
    """usage: int return = km_enable(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_enable(komodo)


# Disable the Komodo.
def km_disable (komodo):
    """usage: int return = km_disable(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_disable(komodo)


# Status mask for km_can_read
KM_READ_TIMEOUT = 0x80000000
KM_READ_ERR_OVERFLOW = 0x40000000
KM_READ_END_OF_CAPTURE = 0x20000000
KM_READ_CAN_ERR = 0x00000100
KM_READ_CAN_ERR_FULL_MASK = 0x000000ff
KM_READ_CAN_ERR_POS_MASK = 0x0000001f
KM_READ_CAN_ERR_POS_SOF = 0x00000003
KM_READ_CAN_ERR_POS_ID28_21 = 0x00000002
KM_READ_CAN_ERR_POS_ID20_18 = 0x00000006
KM_READ_CAN_ERR_POS_SRTR = 0x00000004
KM_READ_CAN_ERR_POS_IDE = 0x00000005
KM_READ_CAN_ERR_POS_ID17_13 = 0x00000007
KM_READ_CAN_ERR_POS_ID12_5 = 0x0000000f
KM_READ_CAN_ERR_POS_ID4_0 = 0x0000000e
KM_READ_CAN_ERR_POS_RTR = 0x0000000c
KM_READ_CAN_ERR_POS_RSVD_1 = 0x0000000d
KM_READ_CAN_ERR_POS_RSVD_0 = 0x00000009
KM_READ_CAN_ERR_POS_DLC = 0x0000000b
KM_READ_CAN_ERR_POS_DF = 0x0000000a
KM_READ_CAN_ERR_POS_CRC_SEQ = 0x00000008
KM_READ_CAN_ERR_POS_CRC_DEL = 0x00000018
KM_READ_CAN_ERR_POS_ACK_SLOT = 0x00000019
KM_READ_CAN_ERR_POS_ACK_DEL = 0x0000001b
KM_READ_CAN_ERR_POS_EOF = 0x0000001a
KM_READ_CAN_ERR_POS_INTRMSN = 0x00000012
KM_READ_CAN_ERR_POS_AEF = 0x00000011
KM_READ_CAN_ERR_POS_PEF = 0x00000016
KM_READ_CAN_ERR_POS_TDB = 0x00000013
KM_READ_CAN_ERR_POS_ERR_DEL = 0x00000017
KM_READ_CAN_ERR_POS_OVRFLG = 0x0000001c
KM_READ_CAN_ERR_DIR_MASK = 0x00000020
KM_READ_CAN_ERR_DIR_TX = 0x00000000
KM_READ_CAN_ERR_DIR_RX = 0x00000020
KM_READ_CAN_ERR_TYPE_MASK = 0x000000c0
KM_READ_CAN_ERR_TYPE_BIT = 0x00000000
KM_READ_CAN_ERR_TYPE_FORM = 0x00000040
KM_READ_CAN_ERR_TYPE_STUFF = 0x00000080
KM_READ_CAN_ERR_TYPE_OTHER = 0x000000c0
KM_READ_CAN_ARB_LOST = 0x00000200
KM_READ_CAN_ARB_LOST_POS_MASK = 0x000000ff
# GPIO Configuration
KM_GPIO_PIN_1_CONFIG = 0x00
KM_GPIO_PIN_2_CONFIG = 0x01
KM_GPIO_PIN_3_CONFIG = 0x02
KM_GPIO_PIN_4_CONFIG = 0x03
KM_GPIO_PIN_5_CONFIG = 0x04
KM_GPIO_PIN_6_CONFIG = 0x05
KM_GPIO_PIN_7_CONFIG = 0x06
KM_GPIO_PIN_8_CONFIG = 0x07
# GPIO Mask
KM_GPIO_PIN_1_MASK = 0x01
KM_GPIO_PIN_2_MASK = 0x02
KM_GPIO_PIN_3_MASK = 0x04
KM_GPIO_PIN_4_MASK = 0x08
KM_GPIO_PIN_5_MASK = 0x10
KM_GPIO_PIN_6_MASK = 0x20
KM_GPIO_PIN_7_MASK = 0x40
KM_GPIO_PIN_8_MASK = 0x80
# Event mask for km_can_read
KM_EVENT_DIGITAL_INPUT = 0x00000100
KM_EVENT_DIGITAL_INPUT_MASK = 0x000000ff
KM_EVENT_DIGITAL_INPUT_1 = 0x00000001
KM_EVENT_DIGITAL_INPUT_2 = 0x00000002
KM_EVENT_DIGITAL_INPUT_3 = 0x00000004
KM_EVENT_DIGITAL_INPUT_4 = 0x00000008
KM_EVENT_DIGITAL_INPUT_5 = 0x00000010
KM_EVENT_DIGITAL_INPUT_6 = 0x00000020
KM_EVENT_DIGITAL_INPUT_7 = 0x00000040
KM_EVENT_DIGITAL_INPUT_8 = 0x00000080
KM_EVENT_CAN_BUS_STATE_LISTEN_ONLY = 0x00001000
KM_EVENT_CAN_BUS_STATE_CONTROL = 0x00002000
KM_EVENT_CAN_BUS_STATE_WARNING = 0x00004000
KM_EVENT_CAN_BUS_STATE_ACTIVE = 0x00008000
KM_EVENT_CAN_BUS_STATE_PASSIVE = 0x00010000
KM_EVENT_CAN_BUS_STATE_OFF = 0x00020000
KM_EVENT_CAN_BUS_BITRATE = 0x00040000
class km_can_info_t:
    def __init__ (self):
        self.timestamp      = 0
        self.status         = 0
        self.events         = 0
        self.channel        = 0
        self.bitrate_hz     = 0
        self.host_gen       = 0
        self.rx_error_count = 0
        self.tx_error_count = 0
        self.overflow_count = 0

class km_can_packet_t:
    def __init__ (self):
        self.remote_req  = 0
        self.extend_addr = 0
        self.dlc         = 0
        self.id          = 0

# Read a single CAN packet from the Komodo data stream.
# This will block for timeout_ms milliseconds; 0 will return
# immediately, and MAXINT will block indefinitely.
# timestamp is in units of nanoseconds.
def km_can_read (komodo, data):
    """usage: (int return, km_can_info_t info, km_can_packet_t pkt, u08[] data) = km_can_read(Komodo komodo, u08[] data)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function.

    Additionally, for arrays that are filled by the API function, an
    integer can be passed in place of the array argument and the API
    will automatically create an array of that length.  All output
    arrays, whether passed in or generated, are passed back in the
    returned tuple."""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # data pre-processing
    __data = isinstance(data, int)
    if __data:
        (data, num_bytes) = (array_u08(data), data)
    else:
        (data, num_bytes) = isinstance(data, ArrayType) and (data, len(data)) or (data[0], min(len(data[0]), int(data[1])))
        if data.typecode != 'B':
            raise TypeError("type for 'data' must be array('B')")
    # Call API function
    (_ret_, c_info, c_pkt) = api.py_km_can_read(komodo, num_bytes, data)
    # info post-processing
    info = km_can_info_t()
    (info.timestamp, info.status, info.events, info.channel, info.bitrate_hz, info.host_gen, info.rx_error_count, info.tx_error_count, info.overflow_count) = c_info
    # pkt post-processing
    pkt = km_can_packet_t()
    (pkt.remote_req, pkt.extend_addr, pkt.dlc, pkt.id) = c_pkt
    # data post-processing
    if __data: del data[max(0, min(_ret_, len(data))):]
    return (_ret_, info, pkt, data)


# Flags mask
KM_CAN_ONE_SHOT = 0x01
# Submit a CAN packet to the Komodo data stream, asynchronously.
def km_can_async_submit (komodo, channel, flags, pkt, data):
    """usage: int return = km_can_async_submit(Komodo komodo, km_can_ch_t channel, u08 flags, km_can_packet_t pkt, u08[] data)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function."""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # pkt pre-processing
    c_pkt = None
    if pkt != None:
        c_pkt = (pkt.remote_req, pkt.extend_addr, pkt.dlc, pkt.id)
    # data pre-processing
    (data, num_bytes) = isinstance(data, ArrayType) and (data, len(data)) or (data[0], min(len(data[0]), int(data[1])))
    if data.typecode != 'B':
        raise TypeError("type for 'data' must be array('B')")
    # Call API function
    return api.py_km_can_async_submit(komodo, channel, flags, c_pkt, num_bytes, data)


# Collect a response to a CAN packet submitted to the Komodo data
# stream, asynchronously.
def km_can_async_collect (komodo, timeout_ms):
    """usage: (int return, u32 arbitration_count) = km_can_async_collect(Komodo komodo, u32 timeout_ms)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_can_async_collect(komodo, timeout_ms)


# Write a stream of bytes to the CAN slave device.  The return
# value of the function is a status code.
def km_can_write (komodo, channel, flags, pkt, data):
    """usage: (int return, u32 arbitration_count) = km_can_write(Komodo komodo, km_can_ch_t channel, u08 flags, km_can_packet_t pkt, u08[] data)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function."""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # pkt pre-processing
    c_pkt = None
    if pkt != None:
        c_pkt = (pkt.remote_req, pkt.extend_addr, pkt.dlc, pkt.id)
    # data pre-processing
    (data, num_bytes) = isinstance(data, ArrayType) and (data, len(data)) or (data[0], min(len(data[0]), int(data[1])))
    if data.typecode != 'B':
        raise TypeError("type for 'data' must be array('B')")
    # Call API function
    return api.py_km_can_write(komodo, channel, flags, c_pkt, num_bytes, data)



#==========================================================================
# GPIO API
#==========================================================================
# Enumeration of input GPIO pin bias configurations.
# enum km_pin_bias_t
KM_PIN_BIAS_TRISTATE = 0x00
KM_PIN_BIAS_PULLUP   = 0x01
KM_PIN_BIAS_PULLDOWN = 0x02

# Enumeration of input GPIO pin trigger edge condition.
# enum km_pin_trigger_t
KM_PIN_TRIGGER_NONE         = 0x00
KM_PIN_TRIGGER_RISING_EDGE  = 0x01
KM_PIN_TRIGGER_FALLING_EDGE = 0x02
KM_PIN_TRIGGER_BOTH_EDGES   = 0x03

# Configure a GPIO pin to act as an input.  The return value
# of the function is a status code
def km_gpio_config_in (komodo, pin_number, bias, trigger):
    """usage: int return = km_gpio_config_in(Komodo komodo, u08 pin_number, u08 bias, u08 trigger)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_gpio_config_in(komodo, pin_number, bias, trigger)


# Enumeration of output GPIO pin driver configurations.
# enum km_pin_drive_t
KM_PIN_DRIVE_NORMAL            = 0x00
KM_PIN_DRIVE_INVERTED          = 0x01
KM_PIN_DRIVE_OPEN_DRAIN        = 0x02
KM_PIN_DRIVE_OPEN_DRAIN_PULLUP = 0x03

# Enumeration of output GPIO pin sources.
# enum km_pin_source_t
KM_PIN_SRC_SOFTWARE_CTL       = 0x00
KM_PIN_SRC_ALL_ERR_CAN_A      = 0x11
KM_PIN_SRC_BIT_ERR_CAN_A      = 0x12
KM_PIN_SRC_FORM_ERR_CAN_A     = 0x13
KM_PIN_SRC_STUFF_ERR_CAN_A    = 0x14
KM_PIN_SRC_OTHER_ERR_CAN_A    = 0x15
KM_PIN_SRC_ALL_ERR_CAN_B      = 0x21
KM_PIN_SRC_BIT_ERR_CAN_B      = 0x22
KM_PIN_SRC_FORM_ERR_CAN_B     = 0x23
KM_PIN_SRC_STUFF_ERR_CAN_B    = 0x24
KM_PIN_SRC_OTHER_ERR_CAN_B    = 0x25
KM_PIN_SRC_ALL_ERR_CAN_BOTH   = 0x31
KM_PIN_SRC_BIT_ERR_CAN_BOTH   = 0x32
KM_PIN_SRC_FORM_ERR_CAN_BOTH  = 0x33
KM_PIN_SRC_STUFF_ERR_CAN_BOTH = 0x34
KM_PIN_SRC_OTHER_ERR_CAN_BOTH = 0x35

# Configure a GPIO pin to act as an output. The return value
# of the function is a status code.
def km_gpio_config_out (komodo, pin_number, drive, source):
    """usage: int return = km_gpio_config_out(Komodo komodo, u08 pin_number, u08 drive, u08 source)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_gpio_config_out(komodo, pin_number, drive, source)


# Set the value of any GPIO pins configured as software controlled
# outputs. The return value of the function is a status code.
def km_gpio_set (komodo, value, mask):
    """usage: int return = km_gpio_set(Komodo komodo, u08 value, u08 mask)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_gpio_set(komodo, value, mask)


# Returns the current values of all GPIO pins.
def km_gpio_get (komodo):
    """usage: int return = km_gpio_get(Komodo komodo)"""

    if not KM_LIBRARY_LOADED: return KM_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_km_gpio_get(komodo)


