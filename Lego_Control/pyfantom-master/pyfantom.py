"""NXT Fantom driver wrapper."""
from ctypes import c_int, c_uint, c_ushort, c_ubyte, c_char_p, c_char, byref, POINTER, Structure, cast
import ctypes.util
import platform
import collections

kMaxFileNameLength = 101
BT_PIN = "1234"
VI_ERROR_IO = -0x4000ffc2        # Equivalent to 0xBFFF003E

DEBUG = True

# Check platform.
if platform.system() == 'Darwin':
    import sys
    if sys.maxsize > 2**32:
        raise RuntimeError("fantom drivers not available in 64 bit mode.\n"
                "You can run python in 32 bit mode using:\n"
                "arch -i386 python2.6\n")
    libpath = '/Library/Frameworks/Fantom.framework/Fantom'
    from AppKit import NSAutoreleasePool, NSApplication
    #libpath = ctypes.util.find_library('Fantom')
else:
    raise RuntimeError('unsupported platform')

# Load library.
dll = ctypes.cdll.LoadLibrary(libpath)
dll.nFANTOM100_createNXTIterator.argtypes = [c_ushort, c_uint, POINTER(c_int)]
dll.nFANTOM100_createNXTIterator.restype = c_uint
dll.nFANTOM100_destroyNXTIterator.argtypes = [c_int, POINTER(c_int)]
dll.nFANTOM100_destroyNXTIterator.restype = None
dll.nFANTOM100_iNXTIterator_advance.argtypes = [c_uint, POINTER(c_int)]
dll.nFANTOM100_iNXTIterator_advance.restype = None
dll.nFANTOM100_iNXTIterator_getNXT.argtypes = [c_uint, POINTER(c_int)]
dll.nFANTOM100_iNXTIterator_getNXT.restype = c_uint
dll.nFANTOM100_iNXTIterator_getName.argtypes = [c_uint, c_char_p,
        POINTER(c_int)]
dll.nFANTOM100_iNXTIterator_getName.restype = None
dll.nFANTOM100_createNXT.argtypes = [c_char_p, POINTER(c_int), c_ushort]
dll.nFANTOM100_createNXT.restype = c_uint
dll.nFANTOM100_destroyNXT.argtypes = [c_uint, POINTER(c_int)]
dll.nFANTOM100_destroyNXT.restype = None
dll.nFANTOM100_iNXT_getFirmwareVersion.argtypes = [c_uint, POINTER(c_ubyte),
        POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_int)]
dll.nFANTOM100_iNXT_getFirmwareVersion.argtypes = None
dll.nFANTOM100_iNXT_getDeviceInfo.argtypes = [c_uint, c_char_p,
        POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_uint), POINTER(c_int)]
dll.nFANTOM100_iNXT_write.argtypes = [c_uint, c_char_p, c_uint,
        POINTER(c_int)]
dll.nFANTOM100_iNXT_write.restype = c_uint
dll.nFANTOM100_iNXT_read.argtypes = [c_uint, c_char_p, c_uint,
        POINTER(c_int)]
dll.nFANTOM100_iNXT_read.restype = c_uint
dll.nFANTOM100_iNXT_pollAvailableLength.argtypes = [c_uint, c_uint, POINTER(c_int)]
dll.nFANTOM100_iNXT_pollAvailableLength.restype = c_uint
dll.nFANTOM100_iNXT_readBufferData.argtypes = [c_uint, c_char_p, c_uint, c_uint,
        POINTER(c_int)]
dll.nFANTOM100_iNXT_readBufferData.restype = c_uint
dll.nFANTOM100_iNXT_sendDirectCommand.argtypes = [c_uint, c_ushort, c_char_p, c_uint,
        c_char_p, c_uint, POINTER(c_int)]
dll.nFANTOM100_iNXT_sendDirectCommand.restype = c_uint
dll.nFANTOM100_iNXT_getDeviceInfo.restype = None
dll.nFANTOM100_iNXT_getResourceString.argtypes = [c_uint, c_char_p,
        POINTER(c_int)]
dll.nFANTOM100_iNXT_getResourceString.restype = None

dll.nFANTOM100_pairBluetooth.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int)]
dll.nFANTOM100_pairBluetooth.restype = None
dll.nFANTOM100_unpairBluetooth.argtypes = [c_char_p, POINTER(c_int)]
dll.nFANTOM100_unpairBluetooth.restype = None
dll.nFANTOM100_isPaired.argtypes = [c_char_p, POINTER(c_int)]
dll.nFANTOM100_isPaired.restype = c_ushort

class FantomException(RuntimeError):
    """Exception thrown on Fantom library error."""
    pass

class Status:
    """Status codes used by Fantom library."""

    # Status codes. {{{
    Success = 0
    Offset = -142000
    PairingFailed = Offset - 5
    BluetoothSearchFailed = Offset - 6
    SystemLibraryNotFound = Offset - 7
    UnpairingFailed = Offset - 8
    InvalidFilename = Offset - 9
    InvalidIteratorDereference = Offset - 10
    LockOperationFailed = Offset - 11
    SizeUnknown = Offset - 12
    DuplicateOpen = Offset - 13
    EmptyFile = Offset - 14
    FirmwareDownloadFailed = Offset - 15
    PortNotFound = Offset - 16
    NoMoreItemsFound = Offset - 17
    TooManyUnconfiguredDevices = Offset - 18
    CommandMismatch = Offset - 19
    IllegalOperation = Offset - 20
    BluetoothCacheUpdateFailed = Offset - 21
    NonNXTDeviceSelected = Offset - 22
    RetryConnection = Offset - 23
    PowerCycleNXT = Offset - 24
    FeatureNotImplemented = Offset - 99
    FWIllegalHandle = Offset - 189
    FWIllegalFileName = Offset - 190
    FWOutOfBounds = Offset - 191
    FWModuleNotFound = Offset - 192
    FWFileExists = Offset - 193
    FWFileIsFull = Offset - 194
    FWAppendNotPossible = Offset - 195
    FWNoWriteBuffers = Offset - 196
    FWFileIsBusy = Offset - 197
    FWUndefinedError = Offset - 198
    FWNoLinearSpace = Offset - 199
    FWHandleAlreadyClosed = Offset - 200
    FWFileNotFound = Offset - 201
    FWNotLinearFile = Offset - 202
    FWEndOfFile = Offset - 203
    FWEndOfFileExpected = Offset - 204
    FWNoMoreFiles = Offset - 205
    FWNoSpace = Offset - 206
    FWNoMoreHandles = Offset - 207
    FWUnknownErrorCode = Offset - 208
    # }}}

    # Text description. {{{
    description = {
            Success: "No error",
            PairingFailed: "Bluetooth pairing operation failed.",
            BluetoothSearchFailed: "Bluetooth search failed.",
            SystemLibraryNotFound: "System library not found.",
            UnpairingFailed: "Bluetooth unpairing operation failed.",
            InvalidFilename: "Invalid filename specified.",
            InvalidIteratorDereference: "Invalid iterator dereference.",
            LockOperationFailed: "Resource locking operation failed.",
            SizeUnknown: "Could not determine the requested size.",
            DuplicateOpen: "Cannot open two objects at once.",
            EmptyFile: "File is empty.",
            FirmwareDownloadFailed: "Firmware download failed.",
            PortNotFound: "Could not locate virtual serial port.",
            NoMoreItemsFound: "No more items found.",
            TooManyUnconfiguredDevices: "Too many unconfigured devices.",
            CommandMismatch: "Command mismatch in firmware response.",
            IllegalOperation: "Illegal operation.",
            BluetoothCacheUpdateFailed: "Could not update local Bluetooth"
            " cache with new name.",
            NonNXTDeviceSelected: "Selected device is not an NXT.",
            RetryConnection: "Communication error.  Retry the operation.",
            PowerCycleNXT: "Could not connect to NXT.  Turn the NXT off and"
            " then back on before continuing.",
            FeatureNotImplemented: "This feature is not yet implemented.",
            FWIllegalHandle: "Firmware reported an illegal handle.",
            FWIllegalFileName: "Firmware reported an illegal file name.",
            FWOutOfBounds: "Firmware reported an out of bounds reference.",
            FWModuleNotFound: "Firmware could not find module.",
            FWFileExists: "Firmware reported that the file already exists.",
            FWFileIsFull: "Firmware reported that the file is full.",
            FWAppendNotPossible: "Firmware reported the append operation is"
            " not possible.",
            FWNoWriteBuffers: "Firmware has no write buffers available.",
            FWFileIsBusy: "Firmware reported that file is busy.",
            FWUndefinedError: "Firmware reported the undefined error.",
            FWNoLinearSpace: "Firmware reported that no linear space is"
            " available.",
            FWHandleAlreadyClosed: "Firmware reported that handle has already"
            " been closed.",
            FWFileNotFound: "Firmware could not find file.",
            FWNotLinearFile: "Firmware reported that the requested file is"
            " not linear.",
            FWEndOfFile: "Firmware reached the end of the file.",
            FWEndOfFileExpected: "Firmware expected an end of file.",
            FWNoMoreFiles: "Firmware cannot handle more files.",
            FWNoSpace: "Firmware reported the NXT is out of space.",
            FWNoMoreHandles: "Firmware could not create a handle.",
            FWUnknownErrorCode: "Firmware reported an unknown error code.",
            }
    # }}}

    @staticmethod
    def check(status):
        """Check status, raise on error."""
        if status.value < Status.Success:
            if status.value in Status.description:
                description = Status.description[status.value]
            else:
                description = 'error %x (hex)' % status.value
            raise FantomException(description)

class StatusVar(Structure):
    """Python wrapper for tStatus."""
    _fields_ = [("value", c_int),
                ("_fileName", c_char * kMaxFileNameLength),
                ("_lineNumber", c_int)]
    
    def __init__(self, code=0):
        """Initialize Status Variable."""
        self.value = code
        
    def __str__(self):
        return str(self.value)

class NXTIterator:
    """Interface to an iterator, to find connected NXT."""

    def __init__(self, search_bluetooth, bluetooth_search_timeout_s=5):
        """Initialize iterator."""
        self.debug = DEBUG
        self.search_bluetooth = search_bluetooth
        self.bluetooth_search_timeout_s = bluetooth_search_timeout_s
        self.handle = None
        self.stop = False
        self.nsapp = None
        self.pool = None
        if platform.system() == 'Darwin':
            self.nsapp = NSApplication.sharedApplication()
            self.pool = NSAutoreleasePool.alloc().init()
        def destroy():
            """To be used in destructor."""
            if self.debug:
                print "pyfantom: Destroying NXTIterator."
            status = StatusVar(0)
            dll.nFANTOM100_destroyNXTIterator(self.handle, cast(byref(status), POINTER(c_int)))
            Status.check(status)
            if self.pool is not None:
                del self.pool
                self.pool = None
            if self.nsapp is not None:
                del self.nsapp
                self.nsapp = None
            if self.debug:
                print "pyfantom: NXTIterator destroyed."
        self.__destroy = destroy

    def __iter__(self):
        """Return the iterator object itself."""
        return self

    def next(self):
        """Implement the iterator protocol."""
        if self.stop:
            raise StopIteration()
        # Find first, or find next.
        status = StatusVar(0)
        if self.handle is None:
            handle = dll.nFANTOM100_createNXTIterator(self.search_bluetooth,
                    self.bluetooth_search_timeout_s, cast(byref(status), POINTER(c_int)))
        else:
            handle = self.handle
            dll.nFANTOM100_iNXTIterator_advance(handle, cast(byref(status), POINTER(c_int)))
        # Check result.
        if status.value == Status.NoMoreItemsFound:
            self.stop = True
            raise StopIteration()
        Status.check(status)
        self.handle = handle
        # Return itself (not part of the protocol, but it has get_nxt and
        # get_name).
        return self

    def get_nxt(self):
        """Get the NXT instance."""
        if self.handle is None or self.stop:
            raise FantomException('invalid iterator')
        status = StatusVar(0)
        handle = dll.nFANTOM100_iNXTIterator_getNXT(self.handle, cast(byref(status), POINTER(c_int)))
        Status.check(status)
        return NXT(handle, self.search_bluetooth)

    def get_name(self):
        """Get the NXT resource name."""
        if self.handle is None or self.stop:
            raise FantomException('invalid iterator')
        status = StatusVar(0)
        name = ctypes.create_string_buffer(256)
        dll.nFANTOM100_iNXTIterator_getName(self.handle, name, cast(byref(status), POINTER(c_int)))
        Status.check(status)
        name = name.value
        return name.upper()

    get_resource_string = get_name

    def __del__(self):
        """Destroy iterator."""
        if self.handle is not None:
            self.__destroy()
        else:
            if self.debug:
                print "pyfantom: No NXTIterator in __del__."

class NXT:
    """Interface to the NXT brick."""

    DeviceInfo = collections.namedtuple('DeviceInfo',
            'name bluetooth_address signal_strength available_flash')

    def __init__(self, name_or_handle, bluetooth=False, pin=BT_PIN):
        """Initialize interface."""
        self.debug = DEBUG
        self.handle = None
        self.isBTLink = bluetooth         # Not used for now
        self.pool = None
        if isinstance(name_or_handle, basestring):
            status = StatusVar(0)
            handle = dll.nFANTOM100_createNXT(name_or_handle, cast(byref(status), POINTER(c_int)),
                    True)
            Status.check(status)
            self.handle = handle
        else:
            self.handle = name_or_handle
        if platform.system() == 'Darwin':
            # Initialize self.pool here to avoid dll.nFANTOM100_createNXT() triggering
            # an autorelease pool error message if it failed
            self.pool = NSAutoreleasePool.alloc().init()
        def destroy():
            """To be used in destructor."""
            if self.debug:
                print "pyfantom: Destroying NXT."
            if self.handle is not None:
                status = StatusVar(0)
                dll.nFANTOM100_destroyNXT(self.handle, cast(byref(status), POINTER(c_int)))
                Status.check(status)
                self.handle = None
                if self.debug:
                    print "pyfantom: NXT destroyed."
            if self.pool is not None:
                del self.pool
                self.pool = None
            else:
                if self.debug:
                    print "pyfantom: NXT handle is None!"
        self.__destroy = destroy

    def get_firmware_version(self):
        """Get protocol and firmware versions installed on this NXT."""
        status = StatusVar(0)
        protocol_major = c_ubyte(0)
        protocol_minor = c_ubyte(0)
        firmware_major = c_ubyte(0)
        firmware_minor = c_ubyte(0)
        dll.nFANTOM100_iNXT_getFirmwareVersion(self.handle,
                byref(protocol_major), byref(protocol_minor),
                byref(firmware_major), byref(firmware_minor),
                cast(byref(status), POINTER(c_int)))
        Status.check(status)
        return (protocol_major.value, protocol_minor.value,
                firmware_major.value, firmware_minor.value)

    def write(self, data):
        """Write, in a generic fashion, to this NXT."""
        status = StatusVar(0)
        data_buffer = ctypes.create_string_buffer(data)
        ret = dll.nFANTOM100_iNXT_write(self.handle, data_buffer, len(data),
                cast(byref(status), POINTER(c_int)))
        if self.debug:
            print "pyfantom: write() sent ", ret, " of ", len(data), " bytes."
        Status.check(status)
        return ret

    def read(self, length):
        """Read, in a generic fashion, from this NXT."""
        status = StatusVar(0)
        data_buffer = ctypes.create_string_buffer(length)
        ret = dll.nFANTOM100_iNXT_read(self.handle, data_buffer, length,
                cast(byref(status), POINTER(c_int)))
        if self.debug:
            print "pyfantom: read() returned ", ret, " of ", length, " bytes."
        try:
            Status.check(status)
        except FantomException as err:
            if status.value != VI_ERROR_IO:
                raise err
        assert ret <= length
        return data_buffer.raw[0:ret]

    def send_direct_command(self, data, responseLength=0, requireResponse=False):
        """Sends the specified direct command to this NXT."""
        """Note: responseLength MUST be set to the exact Data Length or else I/O Error will result."""
        status = StatusVar(0)
        data_buffer = ctypes.create_string_buffer(data)
        response_buffer = None
        if requireResponse:
            response_buffer = ctypes.create_string_buffer(responseLength)
        ret = dll.nFANTOM100_iNXT_sendDirectCommand(self.handle, requireResponse, data_buffer, len(data),
                response_buffer, responseLength, cast(byref(status), POINTER(c_int)))
        Status.check(status)
        if requireResponse:
            if self.debug:
                print "send_direct_command() response: ", struct.unpack('%dB' % len(response_buffer), response_buffer)
            return response_buffer.raw[0:ret-1]    # ret count includes Status byte, but Status byte is not included in message buffer
        else:
            return ""

    def poll_command_length(self, buffer=0):
        """Polls the data buffer on this NXT for the number of bytes available to be read."""
        buffer_selector = c_uint(buffer)
        status = StatusVar(0)
        ret = dll.nFANTOM100_iNXT_pollAvailableLength(self.handle, buffer_selector,
                cast(byref(status), POINTER(c_int)))
        Status.check(status)
        return ret

    def poll_command(self, length, buffer=0):
        """Reads data from the data buffer on this NXT."""
        status = StatusVar(0)
        buffer_selector = c_uint(buffer)
        data_buffer = ctypes.create_string_buffer(length)
        ret = dll.nFANTOM100_iNXT_readBufferData(self.handle, data_buffer, buffer_selector, length,
                cast(byref(status), POINTER(c_int)))
        Status.check(status)
        assert ret <= length
        return data_buffer.raw[0:ret]

    def get_device_info(self):
        """Get basic information about this NXT."""
        status = StatusVar(0)
        name = ctypes.create_string_buffer(16)
        bluetooth_address = (c_ubyte * 7)()
        signal_strength = (c_ubyte * 4)()
        available_flash = c_uint(0)
        dll.nFANTOM100_iNXT_getDeviceInfo(self.handle, name,
                bluetooth_address, signal_strength, byref(available_flash),
                cast(byref(status), POINTER(c_int)))
        name = name.value
        bluetooth_address = ':'.join('%02x' % c
                for c in bluetooth_address[0:6])
        return self.DeviceInfo(
                name = name.upper(),
                bluetooth_address = bluetooth_address.upper(),
                signal_strength = tuple(c for c in signal_strength),
                available_flash = available_flash.value,
                )

    def get_resource_string(self):
        """Get the NXT resource name."""
        status = StatusVar(0)
        name = ctypes.create_string_buffer(256)
        dll.nFANTOM100_iNXT_getResourceString(self.handle, name,
                cast(byref(status), POINTER(c_int)))
        Status.check(status)
        name = name.value
        return name.upper()

    def close(self):
        if self.debug:
            print "pyfantom: close()"
        if self.handle is not None:
            self.__destroy()
        else:
            if self.debug:
                print "pyfantom: No NXT in close()."

    def pair_bluetooth(self, resource, pin=BT_PIN):
        btpin = ctypes.create_string_buffer(256)
        btpin.value = pin
        paired_name = ctypes.create_string_buffer(256)
        status = StatusVar(0)
        dll.nFANTOM100_pairBluetooth(resource, btpin, paired_name, cast(byref(status), POINTER(c_int)))
        Status.check(status)
        paired_name = paired_name.value
        return paired_name.upper()

    def unpair_bluetooth(self, resource):
        status = StatusVar(0)
        dll.nFANTOM100_pairBluetooth(resource, cast(byref(status), POINTER(c_int)))
        Status.check(status)

    def ispaired_bluetooth(self, resource):
        status = StatusVar(0)
        paired = dll.nFANTOM100_isPaired(resource, cast(byref(status), POINTER(c_int)))
        Status.check(status)
        return paired

    def __del__(self):
        """Destroy interface."""
        if self.handle is not None:
            self.__destroy()
        else:
            if self.debug:
                print "pyfantom: No NXT in __del__."

if __name__ == '__main__':
    import struct
    import time
    MAXBUFLEN = 64
    
    def get_nxt_from_iterator(searchBT):
        devicelist = []
        for i in NXTIterator(searchBT):
            devicelist.append(i.get_nxt())
        return devicelist

    def get_resource_string_from_iterator(searchBT):
        resourcelist = []
        for i in NXTIterator(searchBT):
            resourcelist.append(i.get_name())
        return resourcelist

    def get_nxt_from_resource_string(rs):
        return NXT(rs)
    
    def get_nxt_info(i):
        print "resource string:", i.get_resource_string()
        print " firmware version:", i.get_firmware_version()
        print " get device info:", i.get_device_info()

    def play_tone_nxt(i):
        # Play Tone using Send Direct Command
        print "send direct command (tone)..."
        cmd = struct.pack('5B', 0x03, 0x00, 0x08, 0x10, 0x00)
        rep = i.send_direct_command(cmd)
        print "direct command returned ", len(rep), " data bytes"
        time.sleep(1)
        # Play Tone using Send Raw Command
        print "send raw command (tone)..."
        cmd = struct.pack('6B', 0x80, 0x03, 0x00, 0x18, 0x10, 0x00)
        r = i.write(cmd)

    def get_nxt_battery(i):
        # Use Direct Command to read Battery level
        # Write GETBATTERYLEVEL DIRECT_CMD.
        # Query:
        #  DIRECT_CMD: 0x00 (response required: not included in command string)
        #  BATT_LEVEL: 0x0B
        # Response (4 data bytes):
        #  REPLY_CMD: 0x02 (not included in reply string)
        #  BATT_LEVEL: 0x0B
        #  VOLTAGE milivolts
        #  VOLTAGE milivolts
        print "send direct command (battery level)..."
        cmd = struct.pack('1B', 0x0B)
        rep = i.send_direct_command(cmd, 4, True)
        print "direct command returned ", len(rep), " data bytes"
        print "Battery Level", struct.unpack('%dB' % len(rep), rep)

        # Use Send Raw Command to read Battery level
        # Write GETBATTERYLEVEL DIRECT_CMD.
        # Query:
        #  DIRECT_CMD: 0x00 (response required)
        #  BATT_LEVEL: 0x0B
        # Response (4 data bytes):
        #  REPLY_CMD: 0x02
        #  BATT_LEVEL: 0x0B
        #  VOLTAGE milivolts
        #  VOLTAGE milivolts
        print "send raw command (battery level)..."
        cmd = struct.pack('2B', 0x00, 0x0B)
        r = i.write(cmd)
        print "wrote", r
        rep = i.read(MAXBUFLEN)
        print "Battery Level", struct.unpack('%dB' % len(rep), rep)



    def write_read_nxt(i, readbuflen=MAXBUFLEN):
        # Test Variable Sized Reads of reply message
        # Write VERSION SYS_CMD.
        # Query:
        #  SYS_CMD: 0x01
        #  VERSION: 0x88
        print "send raw command (version system command)..."
        cmd = struct.pack('2B', 0x01, 0x88)
        r = i.write(cmd)
        print "wrote", r
        # Response (7 data bytes):
        #  REPLY_CMD: 0x02
        #  VERSION: 0x88
        #  SUCCESS: 0x00
        #  PROTOCOL_VERSION minor
        #  PROTOCOL_VERSION major
        #  FIRMWARE_VERSION minor
        #  FIRMWARE_VERSION major
        rep = i.read(readbuflen)
        print "read", struct.unpack('%dB' % len(rep), rep)

    def read_emptybuf_nxt(i, readbuflen=MAXBUFLEN):
        rep = i.read(readbuflen)
        print "read", struct.unpack('%dB' % len(rep), rep)

    
    # check_bt == True: Bluetooth Interface
    # check_bt == False: USB Interface
    check_bt = True
    get_info = True
    play_tone = True
    get_battery = True
    write_read = True
    empty_readbuf = False
    

    print "Retrieving list of NXT objects"
    nxtlist = get_nxt_from_iterator(check_bt)
    for i in nxtlist:
        print "nxtlist: ", i
        if get_info:
            get_nxt_info(i)
        if play_tone:
            play_tone_nxt(i)
        if get_battery:
            get_nxt_battery(i)
        if write_read:
            write_read_nxt(i)
        if empty_readbuf:
            read_emptybuf_nxt(i)
        i.close()
        del i
    
    print "Creating NXT objects from list of Resource Strings"
    nxtresourcelist = get_resource_string_from_iterator(check_bt)
    for rs in nxtresourcelist:
        print "nxtresourcelist: ", rs
        i = NXT(rs, check_bt)
        if get_info:
            get_nxt_info(i)
        if play_tone:
            play_tone_nxt(i)
        if get_battery:
            get_nxt_battery(i)
        if write_read:
            write_read_nxt(i)
        if empty_readbuf:
            read_emptybuf_nxt(i)
        i.close()
        del i

    exit (0)

