# EON-OpenSlicer – Final Design Report

## Team Name
EON-OpenSlicer

## Team Members
- Mitchell Koski – Computer Science, University of Cincinnati – koskima@mail.uc.edu
- Muhanad Al-Khasawneh – Computer Science, University of Cincinnati – alkhasmr@mail.uc.edu
- Muneer Al-Khasawneh – Computer Science, University of Cincinnati – alkhasme@mail.uc.edu

**Advisor:** Jeremy Hill

---

## Project Topic Area
Development of a web-based platform for the 3D Print Lab, with server integration for cloud-based print management. The system will allow students to submit print jobs online, lab managers to approve and monitor jobs, and admins to manage printer resources, maintenance, and user access.

---

## Project Abstract
EON-OpenSlicer is a centralized 3D printing lab management system designed to streamline the submission, tracking, and completion of print jobs. It improves workflow efficiency by organizing requests, managing printer resources, and providing clear communication between users and operators.

---

## Table of Contents

1. [Project Description (Assignment #2)](./Classwork/assignment2)

2. [User Stories & Design Diagrams (Assignment #4)](./Classwork/assignment4)

3. [Self-Assessment Essays (Assignment #3)](./Classwork/assignent3)

4. Project Tasks & Timeline (Assignments #5–6)
   - [Assignment 5](./Classwork/assignment5)
   - [Assignment 6](./Classwork/assignment6)

5. [ABET Concerns Essay (Assignment #7)](./Classwork/assignment7)

6. [PPT Slideshow (Assignment #8)](./Classwork/assignment8)

7. [Professional Biographies (Assignment #1)](./Classwork/assignment1)

8. [Budget](#budget)

9. [Appendix](#appendix)

---

## Budget
No direct expenses were required for this project. We used personal computers, free software, and university resources.

---

## Effort Summary
All team members met the required effort:

- Mitch: 100+ hours
- Muneer: 68+ hours
- Muhanad: 63+ hours

Work included coding, research, documentation, meetings, and communication through Discord, in person, messaging/emailing, and Teams.

---

## Code Signing for Windows Builds

To prevent Windows SmartScreen warnings about unverified publishers, the EON-OpenSlicer executable can be digitally signed with a code signing certificate.

### For Users

When downloading signed releases, Windows will recognize the verified publisher and not display "unsafe" warnings.

### For Developers

See the comprehensive [Code Signing Documentation](./docs/CODE_SIGNING.md) for:
- How to obtain a code signing certificate
- Setting up GitHub Actions for automated signing
- Signing executables locally
- Troubleshooting common issues

**Quick Start for Local Signing:**

```powershell
# Sign an executable
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "cert.pfx" -CertificatePassword "password"
```

### GitHub Actions Setup

To enable automatic code signing in CI/CD:

1. Obtain a code signing certificate (.pfx format)
2. Convert certificate to Base64
3. Add GitHub repository secrets:
   - `WINDOWS_CERTIFICATE`: Base64-encoded certificate
   - `CERTIFICATE_PASSWORD`: Certificate password
4. The build workflow will automatically sign releases

For detailed instructions, see [docs/CODE_SIGNING.md](./docs/CODE_SIGNING.md).

---

## Appendix
Full code repository:  
https://github.com/Electrovian/Project-EON-OpenSlicer
