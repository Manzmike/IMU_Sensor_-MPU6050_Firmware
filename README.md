# Skyryse Assessment Python Script Overview

## Overall Explanation

This Python script showcases the use of various functionalities such as random selection, Raspberry Pi GPIO integration, and real-time data handling with an IMU sensor (MPU6050). The project aims to control fuel flow into an engine under varying conditions, implementing linear interpolation for angle-based adjustments between 15 and 45 degrees. The script also accommodates static values for other specified angles.

### Key Features

- Integration with an IMU sensor (MPU6050) for real-time data testing, considering its slow sampling rate (~1 second intervals).
- Engine throttle actuation positioning scheduled to achieve a rate close to 10 Hz, enhancing the responsiveness of fuel flow control.

## Hardware Connection Guide

### Required Components

- ITG/MPU MPU6050 Sensor
- Raspberry Pi
- 4 connecting wires

### Connection Steps

1. Connect the VCC pin of the sensor to the 5V pin on the Raspberry Pi.
2. Connect the GND pin of the sensor to a ground (GND) pin on the Raspberry Pi.
3. Connect the SCL pin of the sensor to the SCL pin on the Raspberry Pi.
4. Connect the SDA pin of the sensor to the SDA pin on the Raspberry Pi.

### Communication Protocol

- Utilize the I2C protocol for communication between the Raspberry Pi and the MPU6050 sensor.
- Important: Ensure I2C is enabled in the Raspberry Pi configuration settings.

## MPU6050 Sensor Registers

### Unused Registers

- **PWR MGMT**: Manages the sensor's power settings.
- **SMPLRT DIV**: Controls the sampling rate of the sensor.
- **CONFIG**: Configures additional filters to reduce noise and enhance data quality.
- **INT ENABLE**: Toggles the availability of new data notifications from the sensor.

### Used Registers

- **ACCEL_XOUT**: Outputs acceleration data along the X-axis.
- **ACCEL_YOUT**: Outputs acceleration data along the Y-axis.
- **ACCEL_ZOUT**: Outputs acceleration data along the Z-axis.

## Key Functions

### `Collective_Positioning`

- Processes `Data_Angle` and adjusts the Engine Throttle Actuator Position based on the angle.
- For angles 0-15 degrees and above 45 degrees, static values are used.
- For angles between 15-45 degrees, values are calculated and passed to `linear_interpolation` for further processing.

### `linear_interpolation`

- Calculates threshold values for angles within the 15-45 degree range, aiding in fuel flow control.

### `read_raw_data`

- Reads 16-bit data from the sensor, combining high and low bytes, and converts it to a signed format to fit within a -32768 to 32767 range.

### `Generate_Data`

- Simulates data using the `randrange` function from the `random` module for testing purposes.

### `Setup_Hardware`

- Reads real-world acceleration data from the sensor, converts it to g-force, and calculates the new angle in a 0-180 degree range for easier interpretation.

### `setup`

- The main function for initializing hardware and data handling capabilities, including real or simulated data acquisition and processing at a 10 Hz frequency.

## Testing and Verification

### Testing Approach

- Understand expected inputs and simulate them through the software.
- Test on simpler hardware or Software in the Loop (SITL) systems to ensure reliability.

### Testing Inputs

- Generate data points and simulate various scenarios to validate input handling.

### Testing Outputs

- Step through functions to verify data accuracy.
- Utilize debugging tools like PDB (Python Debugger) or GDB for C programs.
- Analyze output through print statements, Serial Window Viewer, or integrated debugging tools.

### Hardware Testing

- Employ a signal analyzer to confirm correct voltage levels and input/output behavior.

This README provides a comprehensive guide to understanding, connecting, and testing the Python script designed for fuel flow control in an engine using a Raspberry Pi and MPU6050 sensor.

