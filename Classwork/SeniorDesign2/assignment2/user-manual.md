
---

# ✅ user-manual.md (Updated)

```md
# PrintNet User Manual

This manual provides a deeper explanation of how PrintNet works internally and how it supports lab-scale printing.

---

## 🧩 System Overview

PrintNet acts as a middleware layer between:
- Users submitting models
- Slicing logic
- Physical 3D printers

It integrates with:
- OctoPrint (printer control)
- Optional Airtable-based submission systems

---

## 🔁 Print Workflow

1. Student submits a 3D model (STL)
2. Job is approved by lab staff
3. Model appears in PrintNet’s queue
4. Model is sliced into G-code
5. G-code is sent to a printer
6. Printer executes the job

---

## 🖨️ Printer States

Printers may be in one of the following states:
- Idle
- Printing
- Offline
- Error

PrintNet prevents jobs from being sent to unavailable printers.

---

## ⚠️ Error Handling

PrintNet handles errors by:
- Rejecting invalid or unsupported files
- Blocking jobs when printers are offline
- Logging failed prints for review

---

## 📂 Printer Configuration

Printers can be configured using an Excel file:
- Printer name
- OctoPrint URL
- API key
- Bed dimensions

If no file is provided, a default printer profile is created.

---

## 🔗 Airtable Integration (Optional)

PrintNet can:
- Pull approved print jobs
- Update job status automatically
- Synchronize with lab submission portals

This feature is optional and safe to disable.

---

## 🛠 Advanced Usage

- Multiple printers can be managed simultaneously
- Jobs can be queued and distributed
- Logs assist with debugging and analytics

PrintNet is modular and extensible for future development.

