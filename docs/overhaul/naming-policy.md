# EON-OpenSlicer Naming Policy

## Purpose
Lock all shipped naming to first-party branding and avoid upstream project branding in user-facing artifacts.

## Required Product Name
- Primary: `EON-OpenSlicer`
- Short name (internal only): `EON`

## Banned User-Facing Names
- `OrcaSlicer`
- `Orca Slicer`

## Use ONLY AT SETUP and wifi connect module
- `Bambu Studio`
- `Bambu` (unless referencing an actual printer model in a profile catalog)

## Scope
- Desktop UI strings.
- Web UI strings.
- Installer names.
- Documentation screenshots and captions.
- Website copy and metadata.

## Exception Rule
Technical compatibility notes may mention upstream names only in internal engineering docs, never in end-user UI.

## Enforcement
- Block release if banned names appear in shipped UI resources.
- Run text scan in CI before packaging.
