METR4202_Billy_Mach2
====================
Final Lab for METR4202 2014. This Lab incorporates the robot (Billy) created in Lab 1 and the Vision Software created in Lab 2 for the Microsoft Kinect allowing Billy to find items by himself and do whatever Surya requires, whether it be stacking or unstacking cups, sorting tea and/or coffee insta-mixes or "clinking" coffee with panaché.


Clone the repository to your computer.
Everything needs to be installed to work correctly, it has just been divided into groups to make component identification easier and modular.


**
Remember to keep everything up to date with [brew update && brew outdated]
**


Vision Component Installation
=============================

Installation guide for Kinect, Libfreenect, Python 2.7.8 and OpenCV 2.4.9 on a Mac. Almost everything is done in terminal, don’t be afraid, Terminal plays nicely! If you decide to go in blind take some Aspirin with you, otherwise check out this guide to have it installed and working within the hour.

•	Download Apple’s Xcode from the App Store, open and agree to the license, wait for the installation items to finish and then quit Xcode.

•	If you have any version of Python currently installed drag the entire folder to trash and Empty Trash. You do not have to delete your Python scripts or code just the installation.

•	Install Homebrew in Terminal
    [ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"]
    and then install Python through Homebrew using the command
    [brew install python]

•	Before going any further we need to let our computer know which Python we will be working in (Macs actually have a system Python already installed but this isn’t the one we want!). Set the installed Python path before the default path with the command
    [echo export PATH='/usr/local/bin:$PATH' >> ~/.bash_profile]
    Typing [which python] should produce [/usr/local/bin/python]. This means everything
    we install now will be installed to “our” Python.

•	Run commands [brew tap homebrew/python] and [brew tap homebrew/science] to get “access” to some great Brews.

•	Install CMake using the command [brew install cmake].
•	Install GCC using the command [brew install gcc].
•	Install Numpy using the command [brew install numpy].
•	Install Matplotlib using the command [brew install matplotlib].

•	Next we need to install a Python Package Manager. Navigate using the ‘cd’ command to /usr/local [cd /usr/local]. Run the command
    [curl -O https://bootstrap.pypa.io/get-pip.py]
    and then [python get-pip.py] for Python 2.7.

•	Install Matplotlib again (my understanding is that Brew does a system install whereas Pip does a Python install) using the command [pip install matplotlib].
•	Install SciPy using the command [pip install scipy].
•	Install SymPy using the command [pip install sympy].
•	Install Pandas using the command [pip install pandas].
•	Install iPython using the command [pip install ipython].
•	Install PyOpenGL using the command [pip install pyopengl].
•	Install Libfreenect using the command [brew install libfreenect].
•	Install libUSB using the command [brew install libusb].
•	Install libTool using the command [brew install libtool]
•	Link Libfreenect and libUSB using the command [brew link libusb].
•	Install OpenCV using the command [brew install opencv].

•	Plug in the Kinect and enter the command [freenect-glview]. A new window will open showing the view from the Kinect camera.

•	Now, before you can start coding you’ll notice that there is no Python in your Applications folder… Show all Apple hidden files and folders using the command
    [defaults write com.apple.finder AppleShowAllFiles 1]
    The Python IDLE can be found in
    Macintosh HD/usr/local/Cellar/python/{whichever version Homebrew installed, mine is 2.7.8_1}/
    Drag the IDLE into your Dock.
    Hide all Apple hidden files and folders using the command
    [defaults write com.apple.finder AppleShowAllFiles 0].


Woohoo!!! How easy was that!! Now, really the only issue I’ve found, which was with my installation was:

•	When you open the IDLE that you dragged to your Dock, write [import cv]. If you get an ImportError when you run the module, type the following
    [$ sudo ln -s /usr/local/Cellar/jpeg/8d/lib/libjpeg.8.dylib /usr/local/lib/libjpeg.8.dylib]



Dynamixel Turntable Control
===========================
•   Install the relevant driver from [http://www.ftdichip.com/Drivers/VCP.htm]
•   In Terminal navigate to
    /ClonedRepository/Dynamixel_Control/dynamixel-1.0.1 and run
    [python setup.py install]
•   Wire the system up as described in the "Connecting The AX12 Via USB.pdf"
•   Run the TurntableControl.py script to set the speed.
•   The Dynamixel Moitor is a great GUI to see what is going on with the Dynamixel but it isn't able to set or control it. Play around with it and get a feel for it :-)



Lego NXT Istallation
====================
•   Install the Lego NXT drivers found on the Lego website [http://www.lego.com/en-us/mindstorms/downloads/download-software].
•   In terminal install NXT-Python using the command [pip install nxt-python].

These next two installs are USB wrappers that allow for interfacing with the Lego via USB. There are alternate Bluetooth drivers and connections but you'll have to check that out for yourself.

•   In Terminal navigate to
    /ClonedRepository/Lego_Control/pyusb-1.0.0b2 and run
    [python setup.py install]
•   In Terminal navigate to
    /ClonedRepository/Lego_Control/pyfantom-master and run
    [python setup.py install]
•   Replace the motor.py file in /usr/local/lib/python2.7/site-packages/nxt with the motor.py file found in the top level git.



Python Sound Installation / Playing
===================================
•   Download and install PyAudio from [http://people.csail.mit.edu/hubert/pyaudio/].
•   There is a class written in the Sound.py that will allow you to play the audio. It can also be used elsewhere if you require.



Arduino
=======
Download and install Arduino and any Java requirements needed to run the program.



DINING WITH BILLY AND HIS HOLINESS
==================================
Go home, make love to your wives, kiss your children goodnight for tomorrow we dine with BILLY!!!!!

•   Connect the vacuum to the Air Hose and plug it into the USB power board.
•   Plug the USB power board into a mains plug and connect the USB to the USB connector.
•   Connect the USB connector to the Arduino and connect the USB to your computer.
•   Open the Arduino software and then minimize it (to keep your desktop clutter free).

•   Connect the Dynamixel and run the TurntableControl.py script.

•   Make sure that either the NXT has battery power or is plugged into power and charging.
•   Connect the NXT USB to the computer.

•   Connect the Kinect to the computer and set it on a platform about 50cm off the work surface, facing the turntable.
•   Use the Calibration board and kinectCalibration.py script located in the vision folder to calibrate the camera.
•   NB!! Once connected and calibrated DO NOT MOVE! The camera is extemely sensitive and a slight bump could throw the whole vision sensing off.

•   Read "Lab 3.pdf" to get an understanding of the requirements. Take note of how the drink orders are entered in.
•   Open BillyAll.py and just under     if __name__ == '__main__':
edit the menu description.
•   Place the Calibration board onto Billy's frame and run the BillyAll.py file. Wait a few seconds and then remove the Calibration board and watch Billy work.

Enjoy and Good Luck!















