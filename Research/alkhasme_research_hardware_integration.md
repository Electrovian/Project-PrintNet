# Hardware Integration for PrintNet  
Author: Muneer Al-Khasawneh (alkhasme)  
Course: CS 5001 – Senior Design  

## 1. Overview

This document summarizes research related to connecting 3D printers to a central software system.  
Since PrintNet aims to manage multiple printers, the hardware integration layer is important for:

- communicating with printers
- collecting status data (temperatures, progress, errors)
- starting and stopping prints
- monitoring safety conditions

Many university makerspaces and community labs typically connect printers using USB through small dedicated computers (e.g., Raspberry Pi) running controller software. PrintNet can build on similar approaches.

---

## 2. Typical Hardware Setup in 3D Printing Labs

Most shared 3D printer labs commonly use:

- Consumer 3D printers (e.g., Creality, Prusa, etc.)
- A small computer per printer (often a Raspberry Pi)
- USB connection from Pi → printer
- Local network access (Wi-Fi or Ethernet)

The small computer handles communication with the printer firmware and exposes a network interface for software like PrintNet to interact with.

This avoids needing to physically plug SD cards into printers.

---

## 3. Controller Software

Controller software often used in labs includes:

- OctoPrint (open source)
- Klipper-based setups
- Manufacturer-specific controllers

These systems typically provide:

- REST APIs
- Websocket event streams
- Temperature and status reporting
- Print start/stop controls

PrintNet does not need to replace these components. Instead, it can communicate with them and provide a higher-level platform.

---

## 4. Hardware Integration Goals for PrintNet

From a PrintNet perspective, hardware integration includes:

- Connecting to each printer’s controller software
- Reading printer status (progress, temperatures, errors)
- Sending print start/stop/pause commands
- Handling communication failures safely
- Logging data for analytics

This allows PrintNet to manage printers without directly modifying firmware.

---

## 5. Safety Considerations

Common concerns in shared labs:

- prints failing unattended
- overheating components
- bed/nozzle crash risks
- users starting prints incorrectly

Hardware integration should support:

- emergency stop functionality
- status monitoring
- optional camera feeds
- disabling printers marked for maintenance

These features help lab staff manage multiple printers more reliably.

---

## 6. My Role Connection

Based on team assignments, my responsibilities include:

- database management
- hardware integration research and planning

This research supports the hardware side by identifying:

- how PrintNet will talk to printers
- what data can be collected
- what safety and control features are possible

Future work may involve testing communication with an actual printer controller (e.g., OctoPrint API) and structuring database fields around the available hardware data.
