METR4202_Billy_Mach2
====================

Final Lab for METR4202 2014. This Lab will incorporate the robot (Billy) created in Lab 1 and the Vision Software created in Lab 2 for the Microsoft Kinect allowing Billy to find items by himself and do whatever Surya requires, whether it be stacking or unstacking cups, sorting tea and coffee insta-mixes or "clinking" coffee with panaché.

Clone the repository to your computer
Install or update to the latest version of MatLab.


Billy Control via Matlab
========================

To operate matlab on the code for the delta-robot Billy:

•	Add the RWTHMindstormsNXT folder and subfolders to your matlab path.
•	Utilise the functions in the BillyCode subfolder



Vision component installation
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

•	Now, before you can start coding you’ll notice that there is no Python is your Applications folder… Show all Apple hidden files and folders using the command
    [defaults write com.apple.finder AppleShowAllFiles 1]
    The Python IDLE can be found in
    Macintosh HD/usr/local/Cellar/python/{whichever version Homebrew installed, mine is 2.7.8_1}/
    Drag the IDLE into your Dock.
    Hide all Apple hidden files and folders using the command
    [defaults write com.apple.finder AppleShowAllFiles 0].


Woohoo!!! How easy was that!! Now, really the only issue I’ve found, which was with my installation was:

•	When you open the IDLE that you dragged to your Dock, write [import cv]. If you get an ImportError when you run the module, type the following
    [$ sudo ln -s /usr/local/Cellar/jpeg/8d/lib/libjpeg.8.dylib /usr/local/lib/libjpeg.8.dylib]


Now you can run the MatchAll.py function (make sure the Kinect is plugged in!).

** Remember to keep everything up to date with [brew update && brew outdated] **


Dynamixel Turntable Control
===========================
•   Install the relevant driver from [http://www.ftdichip.com/Drivers/VCP.htm]
•   Wire the system up [as described]
•   Run the file to set the speed.



