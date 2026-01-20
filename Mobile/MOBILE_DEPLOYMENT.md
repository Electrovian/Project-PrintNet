# Mobile Deployment Guide

Commands below assume you run them from the repo root.

## Prerequisites

- Python 3.12
- Android: Java 17 and Android SDK/NDK (Briefcase will prompt for setup)
- iOS: macOS with Xcode and iOS SDK

## Build and Package

### Android

```bash
python -m pip install -r Mobile/requirements-mobile.txt
briefcase create android
briefcase build android
briefcase package android --adhoc-sign
```

### iOS

```bash
python -m pip install -r Mobile/requirements-mobile.txt
briefcase create iOS
briefcase build iOS
briefcase package iOS --adhoc-sign
```

## Backend API Expectations

The mobile UI expects a server that exposes basic JSON endpoints:

- `GET /api/mobile/summary` -> `{ "status": "string", "jobs": [ { "id": "...", "name": "...", "status": "..." } ] }`
- `POST /api/jobs/{id}/action` with JSON body `{ "action": "pause|resume|cancel" }`

If these endpoints are not available, the app will show a refresh error but will remain usable.

## App Configuration

- Enter the server URL and optional API token in the mobile UI.
- No local slicing is performed on mobile; slicing must happen server-side.
