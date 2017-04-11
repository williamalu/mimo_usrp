# Multiple Input Multiple Output with Universal Software Radio Peripheral

Introduction to Analog and Digital Communications, Olin College, Spring 2017

## Setup
For this project, we're using an [Ettus B210](https://www.ettus.com/product/details/UB210-KIT) USRP with [GNU Radio](http://gnuradio.org/). Here are instructions for installing GNU Radio in Ubuntu for use with the B210 USRP.

1. Install GNU Radio.
```
apt-get install gnuradio
```

2. Install Ettus' hardware drivers.
```
apt-get install libuhd-dev libuhd003 uhd-host
```

3. Download firmware packages for Ettus USRPs.
```
cd /usr/lib/uhd/utils/
./uhd_images_downloader.py
```

4. Plug the B210 USRP into your computer via USB and check whether or not your computer has properly detected the USRP.
```
uhd_find_devices
```
The resulting output should look something like this:
```
linux; GNU C++ version 5.3.1 20151219; Boost_105800; UHD_003.009.002-0-unknown

-- Loading firmware image: /usr/share/uhd/images/usrp_b200_fw.hex...
--------------------------------------------------
-- UHD Device 0
--------------------------------------------------
Device Address:
    type: b200
    name: MyB210
    serial: <7 character serial number goes here>
    product: B210
```

## Team Members
- [Shane Kelly](https://github.com/shanek21)
- [Franton Lin](https://github.com/frantonlin)
- [William Lu](https://github.com/williamalu)
- [Byron Wasti](https://github.com/byronwasti)
