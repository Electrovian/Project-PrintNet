# Project-PrintNet

Project-PrintNet is a slicer and print workflow codebase with the active application in `App/`.

## Start Here

- `docs/LAUNCH_READINESS.md` for the authoritative repo-wide launch and smoke runbook.
- `App/README.md` for the current app entrypoint, smoke suite, and parity runner.
- `docs/TASKS.md` for the live task tracker.
- `App/Tests/run_tests.py` for the curated smoke and full test entrypoints.

## Common Commands
---
## Project Description
PrintNet is a web-based 3D printing management platform designed for university use. It allows students to upload models, configure print settings through an in-browser slicer, and submit jobs for approval. Administrators can manage queues and printers efficiently. The system improves accessibility, organization, and overall efficiency of shared 3D printing resources.

---

```powershell
cd App
python main.py
python .\Tests\run_tests.py --scope smoke
python -m App.testing.fff_parity --manifest <manifest.json> --profile <profile.json> --output <report.json>
```

Repo-wide launch readiness:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\launch_readiness.ps1
```

The parity command now fails loudly when its corpus meshes are missing and does not return a false-green result when nothing can be compared.
---

## Table of Contents

1. [Project Description (Assignment #2)](./Classwork/assignment2)

2. [User Stories & Design Diagrams (Assignment #4)](./Classwork/assignment4)

3. [Self-Assessment Essays (Assignment #3)](./Classwork/assignent3)

4. Project Tasks & Timeline (Assignments #5-6)
   - [Assignment 5](./Classwork/assignment5)
   - [Assignment 6](./Classwork/assignment6)

5. [ABET Concerns Essay (Assignment #7)](./Classwork/assignment7)

6. [PPT Slideshow (Assignment #8)](./Classwork/assignment8)

7. [Professional Biographies (Assignment #1)](./Classwork/assignment1)

8. [Budget](#budget)

9. [Appendix](#appendix)

---

## Budget

No direct expenses were required for this project. We used personal computers, free software, and university resources(professor Help with code).

---

## Meeting Schedule
The team met regularly every **Tuesday and Thursday from 7:00 PM to 8:00 PM** throughout the project. These recurring meetings were used to review progress, discuss implementation issues, divide tasks, test features, and plan upcoming work. This meeting schedule serves as part of the evidence supporting team effort and collaboration across the semester.

---

## Effort Summary
All team members met the required effort:

- Mitch: 2000+ hours
- Muneer: 60 hours
- Muhanad: 60 hours

Work included coding, research, documentation, meetings, and communication through Discord, in person, messaging/emailing, and Teams.

---

## Appendix
Full code repository:  
https://github.com/Electrovian/Project-EON-OpenSlicer
