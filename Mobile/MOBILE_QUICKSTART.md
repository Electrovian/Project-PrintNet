# Mobile Quickstart

Commands below assume you run them from the repo root.

1. Install dependencies: `python -m pip install -r Mobile/requirements-mobile.txt`
2. Run the mobile preflight: `python -m Mobile.preflight`
3. Create the app: `briefcase create android` or `briefcase create iOS`
4. Build the app: `briefcase build android` or `briefcase build iOS`
5. Package the app: `briefcase package android --adhoc-sign` or `briefcase package iOS --adhoc-sign`
6. Enter your server URL and API token inside the mobile app UI.

The launch target for this demo is the Toga/Briefcase app in `Mobile/app_mobile.py`.
The Flutter runner is experimental and not part of the authoritative launch path.
