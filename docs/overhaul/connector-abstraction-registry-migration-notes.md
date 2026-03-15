# Connector Abstraction and Registry Migration Notes

Date: 2026-02-13  
Checklist ID: `T289`

## Legacy Baseline

- Desktop print dispatch directly used `integrations.octoprint_api.upload_and_print`.
- Connector type routing did not exist.
- Print manager was effectively OctoPrint-only.

## Current Baseline

- Print manager dispatch is routed through connector registry.
- Connector interface and capabilities are explicit and protocol-neutral.
- Legacy OctoPrint behavior is preserved through `octoprint_legacy` bridge connector.
- Offline/local flow exists through `local_file` connector.

## Migration Impact

- Existing flows keep working while connector operations are progressively expanded in later workstreams.
- Connector selection can now be expressed in printer metadata (`connector_type`).
- Future protocol connectors can be added without changing print manager call sites.
