# OctoPrint Overview and How It Relates to EON-OpenSlicer
Author: Muneer Al-Khasawneh (alkhasme)  
Course: CS 5001 – Senior Design  

## 1. What is OctoPrint?

OctoPrint is a web interface for consumer 3D printers that lets you control and monitor a printer from a browser instead of standing at the machine. It’s usually installed on a Raspberry Pi and connected via USB to the printer.

Key features:
- Remote start/pause/stop of print jobs
- Upload G-code through the browser
- Live temperature monitoring
- Optional webcam support
- Plugin ecosystem for extended features

## 2. Architecture

A typical OctoPrint setup includes:
- **Raspberry Pi (OctoPi)** running the OctoPrint server  
- **3D Printer** connected by USB  
- **Web client** accessing OctoPrint via LAN/WiFi  
- **REST API + WebSocket** for external integrations  

## 3. Relevance to EON-OpenSlicer

EON-OpenSlicer can use OctoPrint as the **low-level controller** for each printer:
- Communicate via REST API  
- Read temps, status, print progress  
- Start or cancel prints  
- Retrieve logs and webcam snapshots  

This allows EON-OpenSlicer to focus on:
- Multi-printer dashboards  
- Student-friendly UI  
- Queue management  
- Job history and analytics  

## 4. Strengths & Weaknesses

Strengths:
- Mature, open-source  
- Lots of plugins  
- Well-supported in 3D printing communities  

Weaknesses:
- Designed for one printer per instance  
- UI is complex for beginners  
- Limited built-in fleet management  

## 5. Potential Use in EON-OpenSlicer

EON-OpenSlicer could:
- Poll each OctoPrint instance  
- Build a central dashboard  
- Provide simple "Beginner Modes"  
- Track usage analytics  
- Standardize print presets across printers  

This allows UC’s lab to keep using proven tools while gaining a modern multi-printer management system layered on top.
