# Sport training dataset tool
> Tool build to generate and edit training dataset for sport activity recognition AI.

[![License][gnu-img]][gnu-licence]
![Language][language-img]
![Plateform][plateform-img]

![ScreenShoot][screenshoot-img]

This project is a **Python3 application** designed to generate the training dataset used by AI for automated sport 
activity recognition.

It ensure the following features :
1. Synchronization of the raw data and video recorded during an experimentation.
2. Mark the event seen on the video to tag the raw data.
3. Export the tagged data as a standard training dataset.

## Installation
This application has been built to run on multiple operating system and the installation procedure differ from one to 
another.

To install the application you will have to follow one of these guide :
* [Windows Installation Guide][windows-install-guide]
* [Ubuntu Installation Guide][ubuntu-install-guide]

## Usage example
The application is quite intuitive and easy to use, as a result this part will be focused only on the main operations.

### Prerequisites
First of all you have to conduce some experimentation in order to obtain real data and the associated video feed.

Then, you will have to standardize the raw data to match the [requirements](#raw-data-file-requirement) to use them with
the application.

Any video file format can be use with this application as long as the video codec has been installed on your computer.
The following file format are the most likely to be installed by default on your operating system : .AVI, .WMV, .MOV,
 .MP4.

### Open the application


## Raw data file requirement
The raw data must be standardized and aggregated in a single CSV file in order to be used with this application.

This file must contains at least one of the following parameter in order to synchronize the raw data and the video feed :
* ACC_X -> The accelerometer X axis.
* ACC_Y -> The accelerometer Y axis.
* ACC_Z -> The accelerometer Z axis.

You can also use a previously generated training dataset if all the previous requirements are fulfilled. 

**Example of input data :**

| ACC_X | ACC_Y | ACC_Z | GYR_X | GYR_Y | GYR_Z | ... |
|-------|-------|-------|-------|-------|-------|-----|
| -61   | -11   | -210  | -119  | -236  | -3    | ... |
|  32   | 36    | 176   | -36   | 109   | 223   | ... |
|  54   | 108   | 183   | -143  | -155  | -162  | ... |
| 213   | -80   | -252  | 51    | 244   | -24   | ... |
| 235   | 215   |  188  | 182   | 25    | -45   | ... |
| ...   | ...   | ...   | ...   | ...   | 142   | ... |

Advanced example are also available in the [demo_data](demo_data) directory.


[screenshoot-img]: screenshoot.png
[language-img]:https://img.shields.io/badge/languages-En-green.svg?style=flat-square
[gnu-img]:https://img.shields.io/github/license/lucasgrelaud/liara-sport-training-dataset-tool.svg?style=flat-square
[release-img]:https://img.shields.io/github/release/lucasgrelaud/liara-sport-training-dataset-tool.svg?style=flat-square
[plateform-img]: https://img.shields.io/badge/plateform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg?style=flat-square

[gnu-licence]: LICENSE
[liara]: http://liara.uqac.ca/
[windows-install-guide]: https://github.com/lucasgrelaud/liara-sport-training-dataset-tool
[ubuntu-install-guide]: https://github.com/lucasgrelaud/liara-sport-training-dataset-tool

