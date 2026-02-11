# PrintNet User Manual

This manual provides a detailed explanation of how **PrintNet** works internally and how it supports lab-scale 3D printing operations.

PrintNet is designed to streamline the entire workflow from student submission to completed print by integrating slicing, queue management, and printer communication into one centralized system.

---

## 🧩 System Overview

PrintNet acts as a middleware layer between:

- Users submitting 3D models
- The internal slicing engine
- Physical 3D printers
- Optional lab management systems

It integrates with:

- **OctoPrint** for printer communication and control
- **Optional Airtable-based systems** for submission management

Instead of using separate slicers, email requests, or SD card transfers, PrintNet centralizes everything into one interface.

---

## 🔁 Complete Print Workflow

The standard PrintNet workflow follows these steps:

1. A student submits a 3D model (STL file).
2. A lab manager reviews and approves the submission.
3. The approved job appears in the PrintNet queue.
4. The model is loaded into the system.
5. The model is sliced into G-code.
6. The generated G-code is sent to the selected printer.
7. The printer executes the job.
8. The job status updates to "Completed."

This structured workflow ensures consistency, traceability, and efficiency within the lab.

---

## 🖨️ Printer States

Printers connected to PrintNet may exist in one of the following states:

- **Idle** – Ready to accept a new job  
- **Printing** – Currently executing a job  
- **Offline** – Not reachable or powered off  
- **Error** – Encountered a hardware or print fault  

PrintNet prevents jobs from being sent to printers that are offline or in an error state.

---

## ⚙️ Slicing System

PrintNet includes a built-in slicing engine responsible for converting STL models into G-code.

### Current Prototype Behavior
- Generates a basic outline of the model’s base
- Displays a wireframe preview of the toolpath
- Demonstrates full model-to-printer workflow integration

### Planned Improvements
Future versions will support:
- Multi-layer slicing
- Advanced infill patterns
- Support structure generation
- Enhanced G-code preview visualization

---

## ⚠️ Error Handling & Logging

PrintNet includes basic safeguards:

- Invalid or unsupported files are rejected
- Jobs cannot be sent to unavailable printers
- Failed prints are logged
- Activity logging assists with debugging

Logs can be reviewed to diagnose system issues or printer communication errors.

---

## 📂 Printer Configuration

Printers are configured using a structured configuration file that may include:

- Printer Name
- OctoPrint URL
- API Key
- Bed Dimensions

If no configuration file is provided, PrintNet automatically creates a default printer profile.

This system allows labs with multiple printers to manage all devices within one unified interface.

---

## 🔗 Optional Airtable Integration

PrintNet can integrate with Airtable to:

- Pull approved student submissions
- Automatically update job status
- Sync queue data with lab management portals

This integration is modular and can be enabled or disabled without affecting core slicing and printing functionality.

---

## 🛠 Advanced Usage & Extensibility

PrintNet is designed with a modular architecture, allowing:

- Multi-printer management
- Queue distribution
- Activity logging and diagnostics
- Future scalability

Developers can extend the slicing logic, enhance UI components, or integrate additional lab management features.

---

## 🚀 Future Development

Planned improvements include:

- Full-feature slicing engine
- Role-based access control
- Built-in print cancel/pause controls
- Real-time printer monitoring
- Enhanced analytics and reporting

PrintNet is built to evolve alongside lab needs and technological advancements.
