# Frontend Data Binding for PrintNet
Author: Mo Al-Khasawneh (alkhasmr)

## 1. Overview
Data binding refers to connecting the user interface to backend data so updates show in real-time or near real-time.

Many educational and lab systems use data binding to update job status without refreshing pages.

## 2. Why It Matters
For PrintNet:
- Students need live status updates
- TAs need to see queue changes
- Lab managers need failure notifications

## 3. Approaches
Common options include:
- REST API polling
- WebSocket connections
- Framework-level binding (e.g., React, Vue)

## 4. Planned Usage
PrintNet may use:
- API calls to retrieve job status
- Automatic UI refresh when status changes

## 5. Open Questions
- Will the backend support real-time updates?
- How frequently should polling occur?
