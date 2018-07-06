@ECHO OFF
ECHO Welcome to the installation script!
ECHO
REM Python3 installation procedure
ECHO The Python3.6 installer will run, please follow the
ECHO instruction shown in the new window.
python-3.6.exe
IF %ERRORLEVEL% NEQ 0 (
	ECHO The installation of Python3.6 have been canceled
	ECHO or an error has occurred, you may have to reinstall
	ECHO it manually.
)
REM Video codec installation procedure
ECHO Now you will be prompt to install some video codec used
ECHO by this software, please fulfilled the process.
video-codec.exe
IF %ERRORLEVEL% NEQ 0 (
	ECHO The installation of the video codec have been canceled
	ECHO or an error has occurred, you may have to reinstall
	ECHO it manually.
)
REM PIP dependencies installation
ECHO Some python3 dependencies have to be installed,
ECHO please wait while we are stetting them up.
py -m pip install numpy pyqt5 pyqtgraph ruamel.yaml
IF %ERRORLEVEL% NEQ 0 (
	ECHO The installation of the python3 dependencies have been 
	ECHO canceled or an error has occurred, you may have to 
	ECHO reinstall it manually.
)
PAUSE

