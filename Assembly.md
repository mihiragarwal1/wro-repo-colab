<div align=center>

![banner](./Extra%20Images/Banner.png)

</div>

***

# Build Guide

This is the build guide for WRO Future Engineers team GIGABIT SPACE 2023 solution - GigaBot. It is segmented into ***TBD*** main steps, with more detailed steps within. It assumes you have necessary tools and miscellaneous materials including but not limited to: M2.5, M3 driver bits; a 3D printer; a soldering iron; 20-24 gauge wire; and M2.5, M3 flat/countersunk screws.

Below is a more-or-less detailed step-by-step guide to recreate GigaBot.

***

# Contents

* [Parts List](#parts-list)
* [Chassis Assembly](#chassis-assembly)
* [Jetson Nano Setup](#jetson-nano-setup)
    * [Board Setup, SSHFS, Static IP](#board-setup-sshfs--static-ip)
    * [Enable GPIO & I2C](#enable-gpio-and-i2c)
    * [Install Packages](#package-installation)
    * [Remove GUI, Autologin, & Run-on-startup](#text-only-auto-login--run-on-startup)
    * [Camera Calibration](#camera-calibration)

***

## Parts List


* [ Jetson Nano 4GB Developer Kit](https://www.amazon.in/NVIDIA-945134500000000-Jetson-Nano/dp/B07PZHBDKT/ref=asc_df_B07PZHBDKT/?tag=googleshopdes-21&linkCode=df0&hvadid=397083170813&hvpos=&hvnetw=g&hvrand=17834902022474069661&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9181926&hvtargid=pla-736379876326&psc=1&ext_vrnc=hi)
* 2x [Arducam Raspberry Pi Official Camera Module V2, with 8 Megapixel IMX219 Wide Angle 175 Degree Replacement](https://www.amazon.in/LEEKWI-Raspberry-Camera-Module-Megapixel/dp/B0B5WDPLXW/ref=sr_1_1?keywords=rpi+cam+v2&qid=1695919486&sr=8-1)
* [Intel AX201 WiFi 6 BT 5.1 M.2 2230 with 10in RP-SMA Antenna](https://www.amazon.in/RCC-AX201NGW-Module-Bluetooth-Network/dp/B08131CXHZ) (not required but helpful)
* [Original HobbyWing QuicRun 1060 60A Brushed Electronic Speed ​​Controller](https://robu.in/product/original-hobbywing-quicrun-1625-60a-brushed-electronic-speed-%E2%80%8B%E2%80%8Bcontroller/?gclid=CjwKCAjwyNSoBhA9EiwA5aYlb_xb1pOc5OmoE8hFzLpjYF8EszvWhPInhuI8OJLzJ9mVmAkoGM8_-RoChv8QAvD_BwE)
* [HobbyWing Brushed 55t Motor (55T)](https://www.flipkart.com/lyla-540-35t-brushed-motor-wp-1060-rtr-60a-esc-rc4wd-d90-1-10-rc-car-electronic-components-hobby-kit/p/itmf99bf8fae0f9b?pid=EHKGNX3SUQMFVPTM&lid=LSTEHKGNX3SUQMFVPTMEFCTUI&marketplace=FLIPKART&cmpid=content_electronic-hobby-kit_8965229628_gmc)
* [MG996R Servo](https://robu.in/product/towerpro-mg996r-digital-high-torque-servo-motor/?gclid=CjwKCAjwyNSoBhA9EiwA5aYlb6geMjc8tdLp4JpjM6ChuxiDMqeowtN2mbboQdNtqbLp7cWhDHQzNhoCCxkQAvD_BwE)
* A LiPo balance charger with XT-60 connector, rated for 3S
* [Bonka Power 11.1v 2200mah Lipo battery](https://www.electronicscomp.com/bonka-11.1v-2200mah-35c-3s-lipo-battery?gclid=CjwKCAjwyNSoBhA9EiwA5aYlb5L4m1NkhoOKjTOF6tmf10qY1autVxF3b2DhmZAnl89ZcQIIB-Hb8BoComQQAvD_BwE)
* 2x [DC-DC 5A Adjustable Buck Converter](https://robu.in/product/xl4005-dc-dc-5-32v-adjustable-step-down-5a-buck-power-supply-module/?gclid=CjwKCAjwyNSoBhA9EiwA5aYlb9LUmcIdBRj49ZHu5DseS0lXCwSZFyTztnzszvZfipi4UHHy7j7nuRoCjCoQAvD_BwE)
* [Male 5.5mm DC Barrel Connectors]
* [Male and Female XT60 Connectors](https://robu.in/product/xt60h-male-female-connector-pair-with-housing/?gclid=CjwKCAjwyNSoBhA9EiwA5aYlb36spsORR6mY5bdOZ919OJso-3ojDvyDCfMJYm5zNabIWrGiD5DNmhoCXY4QAvD_BwE)
* [Normally Closed/Momentary On Push Button](https://robu.in/product/red-ds-316-10mm-lock-free-momentary-self-reset-small-push-button-switch/?gclid=CjwKCAjwyNSoBhA9EiwA5aYlbx7_yejxZOzbHwGbsDoJ8aB4PY14HtEr1IvFmg69gaSoR0Pq4DH1ShoCoPAQAvD_BwE) (size must match)
* 20-24 gauge wire
* M3 nylon screws (6mm)
* M3 nylon standoffs (6mm works best)
* M3 nylon nuts
* M3 nuts
* Countersunk, cap head M3 screws (6mm and 8mm work best)


You will need (at least) the following tools:
* 3D printer or access to 3D printing service
* Hex Allen drivers (key or bits)
* Phillips head drivers
* Rotary tool with grinding bit (depending on which version of motor)
* Crimper tool
* Soldering iron

*There may be items not listed that are used in the build guide, we apologize if that happens.*

***

## Chassis Assembly

Sorry! We couldn't get to the assembly instructions in time! Print out the parts located in `/CAD Files/files`. in their given orientation (they have been oriented for the best print results) Most of the assembly should be fairly simple, and follow the pinout sheet linked below and connect to their corresponding pins on the other boards. Some holes may need to be drilled out to make screws fit.


[Jetson Nano pinout sheet](./Others/GPIO_PINOUT.xlsx)

*Note: For I2C connectors, Yellow should be SCL and blue should be SDA; there is no set standard.*


For soldering, we recommend soldering the regulators to their own connectors **in parallel**, and using that as a pass-through to the ESC. The female connectors should be used on the ESC inputs and regulator input, and the male connector on the pass through end of the regulator wires. See the diagram below.

Follow the quick start guide for the ESC to solder the motor connections. Brief summary: solder A, B, and C connectors to the motor (or supplied connectors). Ensure the sensor wire is secure before mounting motor and ESC.

**WARNING:** DO NOT CONNECT THE ESC 3-PIN DIRECTLY TO THE SERVO DRIVER! IT WILL BACKDRIVE THE REGULATOR AND BREAK IT! ONLY CONNECT THE PWM PIN (white)!

***

## Jetson Nano Setup

### Board Setup, SSHFS, & Static IP

Visit [Yahboom](http://www.yahboom.net/)'s [setup and tutorial repository](http://www.yahboom.net/study/jetson-nano) to begin setting up the [Jetson Nano 4GB](https://category.yahboom.net/collections/jetson/products/jetson-nano-sub). Follow steps 1.1-1.7 in "Development setup > SUB Version".

-> http://www.yahboom.net/study/jetson-nano

After setting up the board, follow step 2.1 in section "Basic Settings" to log into your Jetson Nano. Keep PuTTY open, as it will be used for the rest of the setup process. Also keep the IP. For remote file transfer, install sshfs (linux only), or use [sshfs-win](https://github.com/winfsp/sshfs-win) from WinFsp. Follow instructions to mount the Jetson Nano to a network drive. Now upload all contents of the `/Program/` folder into a new folder on the Jetson Nano. Remember the directory of the folder, this will be used later.

*This method should be used to upload programs.*

Make sure a static IP is set to the board to make SSH and file transfer easier. Go to your router settings and [assign a DHCP reservation (PCmag)](https://www.pcmag.com/how-to/how-to-set-up-a-static-ip-address) (or a straight static IP) to your Jetson Nano. Save this IP in your PuTTY settings and SSHFS mounting.

### Enable GPIO and I2C

Next, setting up the board for the application. First, enable GPIO and I2C. Create a new user group, and add your user to it (this is the user running the commands).

```
sudo groupadd -f -r gpio
sudo usermod -a -G gpio your_user_name
```

Copy `99-gpio.rules` from `/misc/` in the project folder to `/etc/udev/rules.d/` on the Jetson Nano. Then enable the rule.

```
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Now enable PWM. Run the options file for jetson-GPIO.

```
sudo /opt/nvidia/jetson-io/jetson-io.py
```

Go down to "Configure 40-pin expansion header" and enter that submenu. Find `pwm0` and `pwm`, and enable them by selecting them and pressing "Enter". Now exit the tool. GPIO and PWM have been enabled.

You may need to enable permissions for I2C

```
sudo usermod -a -G i2c your_user_name
```

### Package Installation

Some packages will need to be installed. [Jetson-GPIO](https://github.com/NVIDIA/jetson-gpio), socket.io-client, [adafruit-servokit](https://github.com/adafruit/Adafruit_CircuitPython_ServoKit), and [adafruit-mpu6050](https://github.com/adafruit/Adafruit_MPU6050) must be installed (Jetson-GPIO may be pre-installed on some versions).

Use the following pip commands:

```
pip3 install adafruit-circuitpython-servokit
pip3 install adafruit-mpu6050
pip3 install "python-socketio[client]"
```

### Camera Calibration

You may encounter pink fringing on the cameras. If that happens, take the following steps to fix it:

Copy `camera_overrides.isp` from `/dist/` in the project folder to `/var/nvidia/nvcam/settings/` on the Jetson Nano.

Give the overrides permissions with the next two:

```
sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
sudo chown root:root /var /nvidia/nvcam/settings/camera_overrides.isp
```

Next, calibrate the cameras. If you skip this step, the distortion correction may have error and the program may not function as intended.

First, you need to run manualdrive and take pictures of a chessboard. Take roughly 10 pictures. Place these pictures in `dist/calibration`, and then run the first cell of `calibrate.ipynb`. The program should print out DIM, K, and D. If there is an error, make sure all the pictures have the full size of the chessboard. Paste these values of DIM, K, and D into the second cell where it says `# Paste matrices here`. Run the second cell to ensure the distortion matrices work. Now you can paste K and D into `converter.py`, at line 25.