# Ubuntu Installation Guide
This guide is made to install the application under the Ubuntu Operating System.

## Python3
This project depends on the third version of the Python interpreter.
In order to run the application you will have to install the interpreter.

1. Open a terminal emulator
2. Type the following line : ```$: sudo apt update && sudo apt install python3 python3-pip```
3. Run the command by pressing the 'Enter' key.

## Gstreamer 
This is the library and service used by PyQT5 to render video in the media player. Because the default Ubuntu installation
does not come with all the required packages, you will have to install them.

1. Open a terminal emulator
2. Type the following line : ```$: list=$(apt-cache --names-only search ^gstreamer1.0-* | awk '{ print $1 }' | grep -v \gstreamer1.0-python3-dbg-plugin-loader)```
3. Run the command by pressing the 'Enter' key.
4. Type the following line : ```$: sudo apt update && sudo apt install $list```
5. Run the command by pressing the 'Enter' key.

## PyQt5 and pyqtqgraph
Because of a specificity of the Ubuntu OS, you will have to install PyQt5 through the default package manager instead of 
PIP3.

1. Open a terminal emulator
2.  Type the following line : ```$: sudo apt update && sudo apt install qt5* libqt5* python3-pyqt5* python3-pyqtgraph```
3. Run the command by pressing the 'Enter' key.

## Python3 Dependencies
The application need some dependencies to be installed to run on a Ubuntu OS.
1. Open a terminal emulator
2.  Type the following line : ```$: sudo pip3 install numpy ruamel.yaml```
3. Run the command by pressing the 'Enter' key.

## Done
The installation process is done, you can finally run the application.