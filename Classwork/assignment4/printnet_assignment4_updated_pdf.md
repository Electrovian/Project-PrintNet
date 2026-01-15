# PrintNet Assignment 4 (PDF)

Source: `PrintNet_Assignment4_UPDATED.pdf`
Original file: `_attachments/printnet_assignment4_updated.pdf`

PrintNet – Assignment #4 (Updated): 
User Stories & Design Diagrams  
Updated: 2025-09-22 19:25 
Design D0 — System Context 
 
Figure 1. D0 – System Context for PrintNet. 
What this shows: who sends inputs to PrintNet (submissions, approvals, admin changes) 
and what outputs they get back (statuses, dashboards, reports, audits).

Design D1 — Major Subsystems & Data Flow 
 
Figure 2. D1 – Major Subsystems and Data Flow. 
 
Inputs/Outputs focus: 
• UI ⇄ API: user actions and responses. 
• API ⇄ DB: job/user/maintenance records (read/write). 
• API ⇄ Slicer: model in → G-code out. 
• API ⇄ Printers: commands out → telemetry/status in. 
• API → UI (events): async notifications. 
 
Design D2 — Detailed Internal Design 
 
Figure 3. D2 – Detailed Backend and Integrations. 
 
Inputs/Outputs focus: 
• UM takes auth inputs from UI; outputs role-gated access; persists to DB; audits to 
AU. 
• JM takes submissions/approvals; outputs queue state; persists to DB; sends model 
to SL (input) and gets G-code (output); enqueues to PM.

• PM outputs printer commands; inputs printer telemetry; forwards usage/errors to 
MM. 
• MM inputs maintenance events; outputs tickets/schedule updates to DB. 
• IN pushes events/webhooks to UI; syncs with Airtable.

ERD — Entities & Relationships 
 
Figure 4. ERD – Data Model for PrintNet.
