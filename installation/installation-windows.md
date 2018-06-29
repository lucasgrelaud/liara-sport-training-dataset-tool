# Windows Installation Guide
This guide is made to install the application under the Windows Operating System.

## Python3
This project depends on the third version of the Python interpreter.
In order to run the application you will have to install the interpreter.

1. Download the latest Python3 installer here : [Python3.7][python3.7-installer]
2. Run the downloaded installer using the administrator right.

## Video codec
By default, the windows OS only come with its own proprietary video codec. Because of that you have to install a bundle 
that contains most of the well use video codec in order to run the application.

1. Download the codec installer here : [K-lite video codec][video-codec-installer]
2. Run the downloaded installer using the administrator right.

## Python3 Dependencies 
The application need some dependencies to be installed to run on a Windows OS.

1. Open a PowerShell prompt with the administrator writes.
2. Type the following line in the prompt : ```pip3.exe install numpy pyqt5 pyqtgraph ruamel.yaml```
3. Run the command by pressing the 'Enter' key.

## Done
The installation process is done, you can finally run the application.

[python3.7-installer]: https://www.python.org/downloads/windows/
[video-codec-installer]: https://www.codecguide.com/download_k-lite_codec_pack_basic.htm