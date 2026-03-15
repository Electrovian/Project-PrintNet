# Contributing

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
python -m pip install -r App/requirements.txt
```

## Tests

```bash
python App/Tests/run_tests.py
```

## Mobile Development

```bash
python -m pip install -r Mobile/requirements-mobile.txt
briefcase create android
briefcase build android
```

## Guidelines

- Keep desktop behavior unchanged unless explicitly requested.
- Prefer small, focused commits and clear commit messages.
- Add or update documentation for new build steps.
