# PicoCalc-Open-Source-Student-Scientific-Calculator
Open source scientific calculator built on Raspberry Pi Pico W — custom PCB, WiFi messaging, IR projector control and games.

# PicoCalc — Open Source Student Scientific Calculator

A fully custom scientific calculator built on the Raspberry Pi Pico W, designed specifically for students. Features wireless peer-to-peer messaging, IR classroom projector control, a custom PCB, and built-in games — all running on MicroPython.

---

## Overview

PicoCalc is an end-to-end hardware and software project encompassing PCB design, embedded systems programming, wireless networking, and circuit design. Every component — from the button matrix to the IR driver circuit — was designed, calculated, and implemented from scratch.

This project was built entirely by a Year 10/11 student as an independent engineering project.

---

## Features

### Scientific Calculator
- Full arithmetic operations with correct operator precedence
- Scientific functions: sin, cos, tan, log, ln, sqrt, powers, factorials
- Degree and radian mode switching
- Expression history and ANS recall
- Error handling for invalid inputs and edge cases
- Custom expression parser built from scratch in MicroPython

### Peer-to-Peer Messaging
- Send and receive text messages between two PicoCalc devices over WiFi
- UDP broadcast protocol for low-latency local communication
- Designed for classroom use — share working, answers, or notes with a friend

### IR Projector Control
- 940nm IR LED with BC547 transistor driver circuit
- Compatible with Hitachi, Maxell, Epson and Samsung projectors and displays
- Up to 10 metre range achieved through transistor amplification
- Allows students to control classroom projectors from their desk
- NEC and SIRC IR protocol support

### Games
- Built-in simple games for use during breaks
- Runs entirely on the calculator hardware — no additional software needed

---

## Hardware

### Custom PCB
- Designed from scratch in KiCad
- Manufactured by PCBWay
- 2-layer PCB with row traces on F.Cu and column traces on B.Cu
- Dimensions: 75.5mm × 146mm

### Components
| Component | Description |
|---|---|
| Raspberry Pi Pico W | Main microcontroller with WiFi and Bluetooth |
| 38× 6mm Tactile Switches | Button matrix (THT, through hole) |
| TSAL6200 | 940nm IR LED, 3mm horizontal |
| BC547 | NPN transistor for IR LED driver |
| 22Ω Resistor | IR LED current limiting |
| 1kΩ Resistor | Transistor base protection |
| 2.42" SSD1309 OLED | 128×64 I2C display |
| 2× AA Battery Holder | MPD BC2AAPC, powers via VSYS |

### Button Matrix
- 38 buttons arranged in a row/column matrix
- GP0–GP7: row outputs
- GP8–GP15: column inputs with internal pull-up resistors
- Only 16 GPIO pins required for 38 buttons
- Scanning rate fast enough to never miss a keypress

### IR LED Circuit
- VSYS (3V from 2× AA) powers the LED circuit
- 22Ω current limiting resistor → 82mA through LED
- BC547 transistor switches the high current safely
- GPIO only supplies <2.6mA to the base — well within Pico's 16mA limit

### Power
- 2× AA batteries connected to VSYS pin
- Auto power-off via MicroPython lightsleep after inactivity
- Lightsleep current draw: ~1-2mA — significantly extends battery life

---

## Software

### MicroPython
- Written entirely in MicroPython
- Modular codebase — calculator, display, networking, IR all separate modules
- Custom expression parser for evaluating scientific expressions
- Uses built-in `math` library for scientific functions

### WiFi Communication
- Both devices connect to the same network
- UDP sockets for low-latency message transmission
- Graceful handling of connection drops and reconnection

---

## PCB Design

Designed in KiCad. Key design decisions:

- **2-layer routing**: Row traces on F.Cu, column traces on B.Cu — allows the button matrix grid to work without short circuits
- **Through hole components**: All buttons and connectors are THT for mechanical strength under repeated use
- **RF keepout zone**: Respected around the Pico W antenna to preserve WiFi/BLE signal strength
- **Removable Pico**: THT header holes allow the Pico W to be plugged in and removed — not permanently soldered
- **Battery on reverse**: Battery holder mounted on B.Cu to keep the front face clean

---

## Schematic & Design Files

- KiCad schematic and PCB layout files included in `/hardware`
- Gerber files included in `/hardware/gerbers`
- BOM included in `/hardware/BOM.csv`

---

## What I Learned

- PCB design and manufacturing process (KiCad → Gerber → PCBWay)
- Ohm's law applied to real circuit design (resistor calculations for IR LED and transistor)
- Button matrix design — why a matrix uses N+M pins instead of N×M
- Two-layer PCB routing and via usage
- MicroPython embedded programming on real hardware
- WiFi networking with UDP sockets on microcontrollers
- IR remote control protocols (NEC, SIRC)
- Debugging real hardware and firmware issues

---

## Project Status

- [x] PCB designed and ordered
- [x] Schematic complete
- [ ] IR LED circuit designed and verified
- [ ] MicroPython calculator engine
- [ ] Display driver integration
- [ ] WiFi messaging
- [ ] IR control implementation
- [ ] Games

---

## License

MIT License — free to use, modify and build upon.
