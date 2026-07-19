# Solarmodbus – Home Assistant Dashboard (Multi‑View)

This folder contains a **multi‑view Home Assistant dashboard** designed to work with the **Solarmodbus** integration.

## Overview

The dashboard is structured into several views:

### 1. Main View: *Overview*
This is the index view, built around the **Sunsynk Power Flow Card**.  
It displays real‑time inverter information including:
- solar production  
- battery charge/discharge  
- load consumption  
- grid import/export  
- MPPT data, voltages, currents  
- autarky and system status  

### 2. Additional Views: *System Work Mode‑1* and *System Work Mode‑2*
These views are **directly inspired by Solarman Cloud** and reproduce its configuration panels:

- Sell to Grid / Zero Export / CT modes  
- Energy pattern (Load First / Battery First)  
- Solar Sell enable/disable  
- Time‑Of‑Use (TOU) day selection  
- TOU charge modes (Grid / Gen)  
- TOU time slots (Start/Stop)  
- Maximum charge power and target SOC  
- All Modbus write actions mapped to buttons  

These views allow **full inverter control** through Modbus (TCP or Solarman) using the scripts provided in the package.

---

## Custom Card Dependencies

Users must install the following Lovelace custom cards (via HACS or manually):

- **sunsynk-power-flow-card**  
- **button-card**  
- **numberbox-card**  
- **card-mod**

No other custom dependencies are required.

---

## Integrating the Solarmodbus Package

The dashboard requires the following directories and file to be added to Home Assistant:

### /homeassistant/packages/solarmodbus/functionality.yaml

This package provides:
- required `input_number` helpers  
- `input_boolean` helpers for TOU days  
- Modbus write scripts (`modbuswrite`, `write_tou_charge_mode`)  
- helper entities used by the dashboard  
- sensors exposed by the Solarmodbus integration  

### Enable packages in Home Assistant

Add this to `configuration.yaml`:

```
homeassistant:
  packages: !include_dir_named packages
