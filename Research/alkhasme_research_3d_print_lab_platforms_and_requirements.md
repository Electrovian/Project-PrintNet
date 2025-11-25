# Existing 3D Printing Management Platforms and Requirements for PrintNet  
Author: Muneer Al-Khasawneh (alkhasme)  
Course: CS 5001 – Senior Design  

## 1. Purpose of PrintNet

PrintNet is intended to be a centralized platform for:
- Managing multiple 3D printers  
- Student print submissions  
- Queueing and job scheduling  
- Lab staff oversight  
- Analytics and reporting  

Many 3D printing labs rely on SD cards, email, or scattered tools to manage prints. PrintNet is designed to provide a more centralized and streamlined workflow.

## 2. Survey of Existing Systems

### **Cloud-based 3D Printer OS Platforms**
Provide:
- Printer fleet dashboards  
- Cloud slicing  
- Remote printing  
- User permissions  
- Analytics  

Examples: MakerFleet-style systems, 3DPrinterOS-type solutions.  
These show what modern labs expect.

### **Manufacturer Ecosystems**
These include:
- Model libraries  
- Cloud slicing  
- Mobile apps  
- Printer-specific control  
Useful inspiration but usually locked to one brand and not made for universities.

## 3. Lessons Learned

Across all platforms:
- Everything is centralized  
- Presets hide advanced slicer settings  
- Real-time monitoring is essential  
- Analytics matter for admins  
- Students need simple workflows  

PrintNet should include these patterns.

## 4. Early Requirements for PrintNet

### **Functional Requirements**
1. User authentication  
2. Role-based permissions  
3. Job submission & queueing  
4. Printer management UI  
5. Status tracking + notifications  
6. Data logging into Airtable  

### **Non-Functional Requirements**
- Beginner friendly  
- Scalable to multiple printers  
- Modular and extensible  
- Secure (prevent job interference)  

## 5. My Role

As the teammate responsible for:
- **Database management**  
- **Hardware integration**  

This research helps define:
- How PrintNet stores data  
- How it communicates with printers  
- How lab analytics and job logs are structured  

This gives us the foundation for PrintNet’s backend architecture.
