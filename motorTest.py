Python 2.7.8 (default, Aug 24 2014, 21:26:19) 
[GCC 4.2.1 Compatible Apple LLVM 5.1 (clang-503.0.40)] on darwin
Type "copyright", "credits" or "license()" for more information.
>>> WARNING: The version of Tcl/Tk (8.5.9) in use may be unstable.
Visit http://www.python.org/download/mac/tcltk/ for current information.

>>> import pyfantom

Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    import pyfantom
  File "/usr/local/lib/python2.7/site-packages/pyfantom.py", line 17, in <module>
    raise RuntimeError("fantom drivers not available in 64 bit mode.\n"
RuntimeError: fantom drivers not available in 64 bit mode.
You can run python in 32 bit mode using:
arch -i386 python2.6

>>> import nxt-python
SyntaxError: invalid syntax
>>> import nxtpython

Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    import nxtpython
ImportError: No module named nxtpython
>>> import npython

Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    import npython
ImportError: No module named npython
>>> ================================ RESTART ================================
>>> 
Bluetooth module unavailable, not searching there

Traceback (most recent call last):
  File "/Users/johnpidgeon/Downloads/nxt-python-2.2.2/examples/spin.py", line 12, in <module>
    b = nxt.locator.find_one_brick()
  File "/usr/local/lib/python2.7/site-packages/nxt/locator.py", line 137, in find_one_brick
    raise BrickNotFoundError
BrickNotFoundError
>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> help(nxt.motor.turn())

Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    help(nxt.motor.turn())
AttributeError: 'module' object has no attribute 'turn'
>>> help(nxt.motor)
Help on module nxt.motor in nxt:

NAME
    nxt.motor - Use for motor control

FILE
    /usr/local/lib/python2.7/site-packages/nxt/motor.py

CLASSES
    __builtin__.object
        BaseMotor
            Motor
            SynchronizedMotors
        OutputState
        SynchronizedTacho
    exceptions.Exception(exceptions.BaseException)
        BlockedException
    TachoInfo
    
    class BaseMotor(__builtin__.object)
     |  Base class for motors
     |  
     |  Methods defined here:
     |  
     |  turn(self, power, tacho_units, brake=True, timeout=1, emulate=True)
     |      Use this to turn a motor. The motor will not stop until it turns the
     |      desired distance. Accuracy is much better over a USB connection than
     |      with bluetooth...
     |      power is a value between -127 and 128 (an absolute value greater than
     |               64 is recommended)
     |      tacho_units is the number of degrees to turn the motor. values smaller
     |               than 50 are not recommended and may have strange results.
     |      brake is whether or not to hold the motor after the function exits
     |               (either by reaching the distance or throwing an exception).
     |      timeout is the number of seconds after which a BlockedException is
     |               raised if the motor doesn't turn
     |      emulate is a boolean value. If set to False, the motor is aware of the
     |               tacho limit. If True, a run() function equivalent is used.
     |               Warning: motors remember their positions and not using emulate
     |               may lead to strange behavior, especially with synced motors
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  debug = 0
    
    class BlockedException(exceptions.Exception)
     |  Method resolution order:
     |      BlockedException
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |  
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.Exception:
     |  
     |  __init__(...)
     |      x.__init__(...) initializes x; see help(type(x)) for signature
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from exceptions.Exception:
     |  
     |  __new__ = <built-in method __new__ of type object>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.BaseException:
     |  
     |  __delattr__(...)
     |      x.__delattr__('name') <==> del x.name
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __reduce__(...)
     |  
     |  __repr__(...)
     |      x.__repr__() <==> repr(x)
     |  
     |  __setattr__(...)
     |      x.__setattr__('name', value) <==> x.name = value
     |  
     |  __setstate__(...)
     |  
     |  __str__(...)
     |      x.__str__() <==> str(x)
     |  
     |  __unicode__(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |  
     |  __dict__
     |  
     |  args
     |  
     |  message
    
    class Motor(BaseMotor)
     |  Method resolution order:
     |      Motor
     |      BaseMotor
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, brick, port)
     |  
     |  brake(self)
     |      Holds the motor in place
     |  
     |  get_tacho(self)
     |  
     |  idle(self)
     |      Tells the motor to stop whatever it's doing. It also desyncs it
     |  
     |  reset_position(self, relative)
     |      Resets the counters. Relative can be True or False
     |  
     |  run(self, power=100, regulated=False)
     |      Tells the motor to run continuously. If regulated is True, then the
     |      synchronization starts working.
     |  
     |  weak_turn(self, power, tacho_units)
     |      Tries to turn a motor for the specified distance. This function
     |      returns immediately, and it's not guaranteed that the motor turns that
     |      distance. This is an interface to use tacho_limit without
     |      REGULATION_MODE_SPEED
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from BaseMotor:
     |  
     |  turn(self, power, tacho_units, brake=True, timeout=1, emulate=True)
     |      Use this to turn a motor. The motor will not stop until it turns the
     |      desired distance. Accuracy is much better over a USB connection than
     |      with bluetooth...
     |      power is a value between -127 and 128 (an absolute value greater than
     |               64 is recommended)
     |      tacho_units is the number of degrees to turn the motor. values smaller
     |               than 50 are not recommended and may have strange results.
     |      brake is whether or not to hold the motor after the function exits
     |               (either by reaching the distance or throwing an exception).
     |      timeout is the number of seconds after which a BlockedException is
     |               raised if the motor doesn't turn
     |      emulate is a boolean value. If set to False, the motor is aware of the
     |               tacho limit. If True, a run() function equivalent is used.
     |               Warning: motors remember their positions and not using emulate
     |               may lead to strange behavior, especially with synced motors
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from BaseMotor:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from BaseMotor:
     |  
     |  debug = 0
    
    class OutputState(__builtin__.object)
     |  An object holding the internal state of a motor, not including rotation
     |  counters.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, values)
     |  
     |  __str__(self)
     |  
     |  to_list(self)
     |      Returns a list of properties that can be used with set_output_state.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class SynchronizedMotors(BaseMotor)
     |  The object used to make two motors run in sync. Many objects may be
     |  present at the same time but they can't be used at the same time.
     |  Warning! Movement methods reset tacho counter.
     |  THIS CODE IS EXPERIMENTAL!!!
     |  
     |  Method resolution order:
     |      SynchronizedMotors
     |      BaseMotor
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, leader, follower, turn_ratio)
     |      Turn ratio can be >= 0 only! If you want to have it reversed,
     |      change motor order.
     |  
     |  brake(self)
     |  
     |  get_tacho(self)
     |  
     |  idle(self)
     |  
     |  reset_position(self, relative)
     |      Resets the counters. Relative can be True or False
     |  
     |  run(self, power=100)
     |      Warning! After calling this method, make sure to call idle. The
     |      motors are reported to behave wildly otherwise.
     |  
     |  turn(self, power, tacho_units, brake=True, timeout=1)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from BaseMotor:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from BaseMotor:
     |  
     |  debug = 0
    
    class SynchronizedTacho(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self, leader_tacho, follower_tacho)
     |  
     |  __str__(self)
     |  
     |  get_target(self, tacho_limit, direction)
     |      This method will leave follower's target as None
     |  
     |  is_greater(self, other, direction)
     |  
     |  is_near(self, other, threshold)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class TachoInfo
     |  An object containing the information about the rotation of a motor
     |  
     |  Methods defined here:
     |  
     |  __init__(self, values)
     |  
     |  __str__(self)
     |  
     |  get_target(self, tacho_limit, direction)
     |      Returns a TachoInfo object which corresponds to tacho state after
     |      moving for tacho_limit ticks. Direction can be 1 (add) or -1 (subtract)
     |  
     |  is_greater(self, target, direction)
     |  
     |  is_near(self, target, threshold)

FUNCTIONS
    get_tacho_and_state(values)
        A convenience function. values is the list of values from
        get_output_state. Returns both OutputState and TachoInfo.

DATA
    LIMIT_RUN_FOREVER = 0
    MODE_BRAKE = 2
    MODE_IDLE = 0
    MODE_MOTOR_ON = 1
    MODE_REGULATED = 4
    PORT_A = 0
    PORT_ALL = 255
    PORT_B = 1
    PORT_C = 2
    REGULATION_IDLE = 0
    REGULATION_MOTOR_SPEED = 1
    REGULATION_MOTOR_SYNC = 2
    RUN_STATE_IDLE = 0
    RUN_STATE_RAMP_DOWN = 64
    RUN_STATE_RAMP_UP = 16
    RUN_STATE_RUNNING = 32


>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> ================================ RESTART ================================
>>> 
>>> 
