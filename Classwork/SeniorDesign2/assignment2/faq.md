# PrintNet FAQ

## Do I need to know how to slice models?
No. PrintNet handles slicing automatically.

---

## What file types are supported?
- STL  
(3MF support is planned but not fully implemented yet.)

---

## What happens if a printer is offline?
PrintNet blocks job submission and alerts the user.

---

## Can multiple users submit jobs at once?
Yes. PrintNet manages a job queue.

---

## Why does the slice preview look simple?
The slicer is currently a prototype and generates a basic outline.
Full slicing features are planned.

---

## Can I cancel a print?
Currently, cancellations are handled through OctoPrint.
Future versions will support canceling directly in PrintNet.

---

## Is this secure?
Security relies on:
- OctoPrint API keys
- Airtable API keys
- Restricted lab machine access

Role-based access is planned for future versions.

---

## Is PrintNet open-source?
Yes. The project is designed to be extended and improved by developers.

