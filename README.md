<div align=center>

![banner](./img/banner.png)

</div>

***

**Official GitHub repository for WRO USA Future Engineers team GIGABIT SPACE 2023. All code, documentation, and files are located here.**

***

# Contents
* [Hardware](#hardware-documentation)
    * [Assembly Instructions & Diagrams](#assembly)
    * [Photos](#photos)
* [Uploading Programs](#uploading-programs)
* [Software](#software-documentation)
    * [Operating System](#operating-system)
    * [Programming Language](#programming-language)
    * [Code Documentation](#code-documentation)
* [Team Photos!!](#team-photos)
* [Demonstrations](#demonstration-video)


***

# HARDWARE

## ASSEMBLY

Shortened assembly instructions:
1. Print 3D models
2. Assemble rear axle
3. Solder electronics
4. Assemble steering mechanism
5. Attach main platform
6. Attach electronics
7. Attach upper platform

#### **For an actual build guide, go to [Assembly.md](./Assembly.md)**

Here is a simple schematic for how the electronics are wired:

![Wiring schematic](./img/docs/wiring-schematic.png)

## Photos
|                                |                                  |
| ------------------------------ | -------------------------------- |
| ![front](./img/docs/front.jpg) | ![back](./img/docs/back.jpg)     |
| ![left](./img/docs/left.jpg)   | ![right](./img/docs/right.jpg)   |
| ![top](./img/docs/top.jpg)     | ![bottom](./img/docs/bottom.jpg) |

***

# Uploading Programs

Make sure you have gone through the [Jetson Nano setup](./ASSEMBLY.md#jetson-nano-setup) steps and set your static IP, have some form of sshfs, and created the program directory. To upload the program, simply copy the contents of the "Program" into the remote directory. **Do not delete the previous directory; you will have to re-install packages!**

***

# Software Documentation

## Operating System

We used the Jetson Nano's existing operating system, which is Ubuntu 18.04 with Jetpack. It has been changed to text-only mode to remove the unnecessary GUI. We also added a startup script ([see "Board Setup" in ASSEMBLY.md](./ASSEMBLY.md#board-setup-sshfs-and-static-ip)) to run the program on startup, which waits for a button press before running the program.

***

## Programming Language

All our code is in python (except the GIGABIT SPACE Control Panel and GIGABIT SPACE Randomizer, those are HTML/JS/CSS applications used for development).

Dependencies:
* Jetson-GPIO
* jetcam
* numpy
* cv2
* adafruit-servokit
* adafruit-circuitpython-mpu6050
* python-socketio
* math
* asyncio
* typing
* traceback
* os
* base64
* time
* threading

The **entire** `Program` directory must be uploaded in order for the program to run. Ensure the `path` constant in `startup.py` is defined properly.

Example:
    `/home/mihir/Desktop/wro-repo-colab/Code_Main/Program/`

***

## Code Documentation

See [DOCS.md](./DOCS.md).

***
