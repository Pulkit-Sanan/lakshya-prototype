# Automated Targeting System

## CPG Number: 211

### Team Members

- Pulkit Sanan (102103239)
- Samriddh Raman Bhatla (102103256)
- Gitesh Budhiraja (102283004)
- Shivam Verma (102103252)

### Mentors

- Dr. Sumit Kumar Aggarwal
- Dr. Sachin Kansal

## Table of Contents

- [Project Overview](#project-overview)
- [Need Analysis](#need-analysis)
- [Related Works / Literature Survey](#related-works--literature-survey)
- [Problem Statement & Objectives](#problem-statement--objectives)
- [Assumptions & Constraints](#assumptions--constraints)
- [Project Execution Plan / Methodology](#project-execution-plan--methodology)
- [Problem Requirements & Outcomes](#problem-requirements--outcomes)
- [Work Plan & Individual Roles](#work-plan--individual-roles)
- [Mechanical Assembly](#mechanical-assembly)
- [Requirements](#requirements)
  - [Mechanical Components](#mechanical-components)
  - [Electronics Components](#electronics-components)
  - [Miscellaneous Components](#miscellaneous-components)
- [Connection Diagram](#connection-diagram)
- [Software Setup](#software-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## Project Overview

The Automated Targeting System (ATS) is an innovative solution that autonomously detects, tracks, and targets subjects with precision, redefining security and defense operations. It integrates advanced sensor and imaging technologies with real-time detection and monitoring algorithms, optimizing control and movement mechanisms to ensure precise and reliable targeting. The ATS aims to address the inefficiencies and complexities of conventional targeting techniques, providing a robust and adaptable solution suitable for various security and defense applications.

## Need Analysis

- Conventional techniques are inefficient and result in heavy collateral damage in armed conflicts.
- Security threats are becoming increasingly complex and varied.
- There is a lack of successful indigenous deterrent systems.
- Improving targeting is essential to optimize operational effectiveness.
- A mentor visit to the Army General Cantonment in Jalandhar identified the problem, as highlighted by Army personnel.

## Related Works / Literature Survey

1. **Lockheed Martin Sniper Advanced Targeting Pod (ATP)**: A precision targeting pod used in military aircraft for long-range target detection, tracking, and engagement.
2. **L3Harris WESCAM MX-Series EO/IR Turrets**: Targeting systems used in airborne surveillance and maritime domains.
3. **Raytheon Technologies - Multi-Spectral Targeting Systems (MTS)**: A family of multi-spectral imaging and targeting systems used in military aircraft.

## Problem Statement & Objectives

**Problem Statement:**
To develop a targeting system that is:
- Autonomous
- Precise
- Adaptable
- Reliable & Robust

**Objectives:**
- Develop an Automated Targeting System (ATS) prototype.
- Integrate sensor and imaging technologies.
- Implement real-time detection and monitoring algorithms.
- Optimize control and movement mechanisms.
- Produce detailed testing and validation reports.

## Assumptions & Constraints

**Assumptions:**
- The mechanical assembly is static.
- Single target detection.
- The target is assumed to be 5m-50m away.

**Constraints:**
- Open-loop system.
- Movement precision at the cost of other parameters.

## Project Execution Plan / Methodology

1. **Prototype Development**: 3D-printed scaled model for testing & validating mechanical assembly & electronic circuitry.
2. **Fabrication**: MS Assembly, sensors, and actuators.
3. **Input Calibration**: Synchronizing input streams via software transformations & circuitry.
4. **Development & Integration**: Algorithmic implementation.
5. **Testing & Validation**: Black & White box rigorous testing & validation.

## Problem Requirements & Outcomes

**Requirements:**
- Mechanical: MS Plates (12mm), Thrust Bearing, Ball bearing, Square Pipes, Fabrication.
- Electronics: Stepper Motors, Motor Drivers, Laser & Heat Sink, Jetson Nano, IC circuitry.
- Software: CAD (Fusion 360), IDE (VS Code), Anaconda, Eagle.

**Outcomes:**
1. Solution to security personnel needs.
2. Indigenous deterrent system.
3. Low-cost computer vision-based solution.
4. Adaptable & applicable to various use cases.

## Work Plan & Individual Roles

- **Designing CAD models**: Samriddh Raman Bhatla, Shivam Verma, Pulkit Sanan
- **Mechanical model fabrication**: Pulkit Sanan, Samriddh Raman Bhatla
- **Electronics**: Samriddh Raman Bhatla
- **Jetson Nano**: Gitesh Budhiraja, Samriddh Raman Bhatla
- **Developing Tracking Model**: Shivam Verma, Pulkit Sanan, Gitesh Budhiraja
- **Documentation & research**: Shivam Verma, Pulkit Sanan, Samriddh Raman Bhatla, Gitesh Budhiraja

## Mechanical Assembly

**Final Approach:**
The mechanical assembly was initially designed with a grooved disc and screw gauge mechanism. However, due to issues with slipping and control difficulties, the design was redesigned to a belt and pulley system for improved control. The final assembly includes:
- Two flywheels mounted on a rod to provide rotation.
- Equipment mounted on a flat surface cut from the rod.
- The entire assembly is mounted on a four-legged stand made from square pipes using universal bearings.
This design ensures effective rotation in the horizontal axis and resolves previous issues.

## Requirements

### Mechanical Components

- Solid MS Base 1.5 foot x 1.75 foot
- Bearing
- Disc (Raw Material 1.25 foot x 1.25 foot)
- MS Rods Dia 2.75 Inch Length 1.5 foot
- Square Support Pipe 1.5 m (Mounting too)
- Screws/Nuts/Standoffs
- Rubber Belt
- Pulleys
- Motor Mount
- Cooling Fan
- Laser Pointer Heatsink 12mm

### Electronics Components

- Stepper Motor Nema 23HS-19kg-cm
- Stepper Motor Driver
- Power Supply 24V/10A
- Laser Pointer 5mW
- Video Camera 64MP AutoFocus CSI
- 50mm C mount Lens for Camera module
- Camera Module with C-mount adapter 12.3 MP
- Nvidia Jetson Nano
- MicroSD Card
- Voltage Stabilizer Module
- Buck Converter DC24V to DC12V
- Thermal Compound, Heat sink, ICs (Electronic supplies)
- Electronic Supplies (Switches, Wires, ICs, etc)

### Miscellaneous Components

- Screws/Nuts/Standoffs
- Electronic Supplies (Switches, Wires, ICs, etc)

## Connection Diagram

For detailed instructions on connecting the electronic circuitry, please refer to the [tutorial](link-to-pdf).

## Software Setup

1. **Arduino IDE:** Download and install the [Arduino IDE](https://www.arduino.cc/en/software).
2. **Python:** Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
3. **OpenCV:** Install OpenCV for Python by running `pip install opencv-python`.
4. **YOLO:** Download the YOLO weights and configuration files from the [official YOLO repository](https://github.com/AlexeyAB/darknet).

## Usage

1. **Setup Arduino:**
   - Upload the provided Arduino code to the Arduino Mega.

2. **Run Python Script:**
   - Execute the Python script to start the YOLO object detection and control the stepper motors.

3. **Manual Control:**
   - Use the buttons connected to the Arduino for manual control of the laser pointer.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References

- [Sniper ATP, Superior Targeting Capability](https://www.lockheedmartin.com/en-us/products/sniper.html)
- [L3Harris WESCAM MX-Series](https://www.l3harris.com/all-capabilities/wescam-mx-series)
- [Raytheon Multi-Spectral Targeting System](https://www.rtx.com/raytheon/what-we-do/air/mts)

Thank you!

---