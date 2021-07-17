# Duet RepRapFirmware plugin for filament load cell

* requires RepRapFirmware 3.3.0 with matching SBC software for DuetWebControl and DuetControlServer
* requires a I2C sensor attached to the SBC that reads a HX711 load cell sensor

This plugin allows you to display the amount or weight of filament spool on your
3D printer. You can quickly judge how much material you have left on this spool
before starting a print job.

![Screenshot of the new weight field in DWC](/dwc-screenshot.png)

![CAD model of the spool holder with integrated load cell](/cad-model.png)

This plugin can be installed via DuetWebControl. It will register a new HTTP
endpoint that exposes a current weight reading of the load cell. The value will
be updated and polled into the browser window every few seconds and displayed in
the top menu bar.

## Hardware

* "bar style" load cell
  - with differential resistor pairs
  - rated weight for 1kg (5kg might work with less accuracy)
  - approx. 80x13x13mm
  - 2 M5 and 2 M4 mounting holes
* HX711 module
* Microcontroller: Arduino Nano or similar ATmega168-powered module
* 3D printer with Duet and RepRapFirmware and SBC

Expected measurement accuracy / usable resolution: +/- 10g for a 1kg spool.

The HX711 load cell amplifier module requires precise timing to read a
measurement. While a Raspberry Pi could do this directly, it is more reliable to
have a dedicated cheap microcontroller perform this timing-critical task and
buffer the measurement values. A Raspberry Pi can then simply query the most
recent and valid measurement via I2C.

## Hardware Integration

* Connect load cell to HX711
  - connect exciter leads to E+ and E-
  - connect amplifier leads to A+ and A-
  - see https://www.instructables.com/Arduino-Scale-With-5kg-Load-Cell-and-HX711-Amplifi/
* Connect HX711 to microcontroller with P_DOUT and P_SCK pins
  - HX711 on VCC connect to Arduino Nano on 3.3V
  - HX711 on GND connect to Arduino Nano on GND
  - HX711 on DT connect to Arduino Nano on D5
  - HX711 on SCK connect to Arduino Nano on D6
  - see https://www.makerguides.com/arduino-nano/#arduino-nano-pinout
* Connect microcontroller via I2C to SBC Raspberry Pi
  - Arduino Nano on A4 connect to SBC on SDA1 / GPIO2 / Pin 3 
  - Arduino Nano on A5 connect to SBC on SCL1 / GPIO3 / Pin 5
  - Arduino Nano on 3.3V connect to SBC on 3.3V / Pin 1
  - Arduino Nano on GND connect to SBC on GND / Pin 9 or others
  - see https://pinout.xyz/pinout/i2c

## Software Setup
* Flash microcontroller `hx711-to-i2c` firmware 
  - using PlatformIO
* Enable I2C on SBC (assuming Raspberry Pi)
  - `sudo raspi-config` - Interfacing Options - I2C
* Install `python3-smbus` on SBC
  - `sudo apt install python3-smbus`
* Install Python APIs for DSF on SBC
  - `sudo pip3 install dsf-python`
* Install Duet RepRapFirmaware plugin
  - via DWC "Upload & Print" button drag & drop.

## License

This project is made available under the MIT License. For more details, see the
``LICENSE`` file in the repository.

## Author

This project was created by Thomas Kriechbaumer.
