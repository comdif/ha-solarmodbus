# TODO – V2 Overview and Core Objective

V2 will primarily focus on replacing the existing cloud‑based configurators with a fully local, transparent, and deterministic configuration workflow.
The goal is to eliminate any dependency on remote services and ensure that all inverter configuration logic is handled locally and reproducibly.
YAML definition files will remain the foundation of the integration, and V2 development will initially target the **Deye hybrid inverter**, which is currently the only model available for real‑world validation.

**Support for additional inverter models will depend on future contributors and access to actual hardware.**

## TODO Technical Notes for V2

- (sensor.py) Introduce a short and generic entity namespace: change `"Solarmodbus Device"` to `"solar"` to simplify entity IDs.
