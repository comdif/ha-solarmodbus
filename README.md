# ha-solarmodbus V2

**Local Modbus integration for Solarman‑compatible inverters (Deye, Sunsynk, LuxPower, Sofar…).  
100% local · Multi‑brand · YAML‑driven · No cloud required**

---

# 🚀 Major New Features in V2

### ✔️ **Native support for the original Deye/Sunsynk Solarman dongle**  
Solarmodbus V2 can communicate **directly with the OEM WiFi/LAN dongle**,  
using the local Solarman V5 protocol — **no cloud**, **no gateway**, **no API keys**.

This is enabled through the official Python library:

### 🔗 `pysolarmanv5` by jmccrohan  
https://github.com/jmccrohan/pysolarmanv5

The integration now supports:

- direct local communication with the Solarman V5 dongle  
- automatic detection of inverter model  
- stable polling without Modbus TCP hardware  
- full compatibility with Deye/Sunsynk OEM dongles

---

## 📌 Important Notice

Solarmodbus V2 also uses the **public inverter register definitions** from the  
**Solarman Python project by Stephan Joubert** (`inverter_definitions/`).

These YAML files are used **only as reference material** for Modbus register mapping.  
All Home Assistant code is **entirely original**.

Original project:  
https://github.com/StephanJoubert/solarman

---

## 🧪 Hardware Used for Testing

### ✔️ **Deye/Sunsynk OEM Solarman V5 dongle**  
Validated for full local operation via `pysolarmanv5`.

### ✔️ **Ebyte NA111‑E Modbus TCP → RS485 gateway**  
Validated for Modbus TCP operation.

### ✔️ **FTDI USB‑RS485 adapter**  
Validated for direct Modbus RTU.

All three modes are fully supported in V2.

---

## 📌 Overview

Solarmodbus V2 is a fully local Home Assistant integration that reads and decodes  
Modbus data from Solarman‑compatible inverters using:

- **Solarman V5 local protocol (OEM dongle)**  
- **Modbus TCP**  
- **Modbus RTU**

V2 introduces a clean, modular architecture:

- unified YAML V2 register definitions  
- stable coordinator  
- modular parsing engine  
- multi‑brand support  
- fast multi‑range polling  
- zero cloud dependency

---

## ✨ Features (V2)

- 🔌 Solarman V5 local protocol (OEM dongle)  
- 🔌 Modbus TCP & RTU  
- ⚡ Optimized multi‑range polling  
- 📄 Unified YAML V2 register definitions  
- 🔍 Advanced parsing engine  
  - endianness  
  - bitmask  
  - multi‑register values  
  - offsets  
  - string decoding  
- 🏠 Native Home Assistant entities  
- 🧱 Clean architecture (coordinator + parser + loader)  
- 🛠️ Easily extensible for new inverter models  

---

## 🚧 Current Status

- ✔️ Fully working on **Deye LP1 / Hybrid**  
- ✔️ Full support for **OEM Solarman V5 dongle**  
- ✔️ YAML V2 ready for multi‑brand support  
- ⏳ Additional inverter definitions in progress  
- 🤝 Community contributions welcome  

---

## 📥 Installation

### 🟦 HAOS

Just past this one-line on you ssh console:

`unzip -o <(curl -fsSL https://github.com/comdif/ha-solarmodbus/archive/refs/heads/v2.zip) -d /tmp \
  && cp -r /tmp/ha-solarmodbus-v2/solarmodbus /config/custom_components/ \
  && ha core restart`

-    How to install on other OS:

Just copy the solarmodbus directory in your HA custom-component directory.

-    How to install on ANY OS with an universal installer:

`bash <(curl -fsSL https://raw.githubusercontent.com/comdif/ha-solarmodbus/refs/heads/v2/uinstall.sh) \
  https://github.com/comdif/ha-solarmodbus/archive/refs/heads/v2.zip
`
