# Local Wi-Fi Onboarding Flow Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T324`

## Guard/Error Cases

- `WIFI_TIMEOUT_INVALID`
  - Trigger: `timeout_s <= 0`.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_MAX_TARGETS_INVALID`
  - Trigger: `max_targets <= 0`.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_HOSTS_REQUIRED`
  - Trigger: discovery called with empty/invalid host list.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_PORT_INVALID`
  - Trigger: any scan port outside `1..65535`.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_PORTS_REQUIRED`
  - Trigger: normalized port list becomes empty.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_CIDR_REQUIRED`
  - Trigger: CIDR discovery called with empty CIDR string.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_CIDR_INVALID`
  - Trigger: CIDR parsing fails.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_CIDR_NO_HOSTS`
  - Trigger: CIDR yields no host addresses.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_HOST_LIMIT_INVALID`
  - Trigger: CIDR host limit <= 0.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_PROBE_INVALID`
  - Trigger: custom probe hook returns non-mapping payload.
  - Handling: raise `LocalWifiOnboardingError`.

- `WIFI_TARGET_TRUNCATED`
  - Trigger: discovery target generation exceeds `max_targets`.
  - Handling: warning is emitted in discovery report; scan proceeds with bounded subset.
