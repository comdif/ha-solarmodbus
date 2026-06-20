# ha-solarmodbus

**Local Modbus integration for Solarman‑compatible inverters (Deye, Sunsynk, LuxPower, Sofar…).  
100% local · Multi‑brand · Extensible · No cloud required**

---

## 📌 Important Notice

This integration uses the **public inverter register definitions** from the  
**Solarman Python project by Stephan Joubert**, specifically the directory: inverter_definitions/

These YAML files are used **as reference material** for Modbus register mapping.  
This project is **not** a fork of his work, and all Home Assistant code here is entirely original.

Original project:  
https://github.com/StephanJoubert/solarman

---

## 🧪 Hardware Used for Testing

All development and validation were performed using:

### ✔️ **Ebyte NA111-E Modbus TCP → RS485 gateway**  
Product page:  
https://www.cdebyte.com/products/NA111-E

This device was used to test:

- Modbus TCP communication  
- multi‑range polling  
- register decoding  
- stability and timing  
- compatibility with Deye Hybrid inverters  

### ✔️ **FTDI USB‑RS485 adapter (direct connection)**

The integration also works **without any gateway**, using a simple USB‑RS485 FTDI adapter connected directly to the inverter’s RS485 port.

This allows:

- direct Modbus RTU → Home Assistant communication  
- testing without network hardware  
- debugging register responses  
- validating wiring and polarity  

Both methods are fully supported.

---

## 📌 Overview

**solarmodbus** is a fully local Home Assistant integration designed to read, decode, and expose Modbus TCP data from hybrid inverters compatible with the *Solarman* ecosystem.

Unlike cloud‑based Solarman solutions, this integration communicates **directly with the inverter over Modbus TCP**, providing:

- fast and stable updates  
- zero cloud dependency  
- no external accounts or API keys  
- full data ownership  
- multi‑brand support through YAML register definitions  

The integration uses a flexible architecture based on YAML files describing the Modbus register maps for each inverter brand/model. This makes it easy for the community to contribute additional definitions and expand compatibility.

---

## ✨ Features

- 🔌 **Direct Modbus TCP communication** (no cloud, no API keys)  
- ⚡ **Fast updates** with multi‑range polling  
- 🧩 **Multi‑brand architecture** (Deye, Sunsynk, LuxPower, Sofar…)  
- 📄 **YAML‑based register definitions**  
- 🔍 **Advanced parsing engine**  
  - endianness handling  
  - Solarman rule system  
  - bitmasks  
  - offsets  
  - string decoding  
  - multi‑register values  
- 🏠 **Native Home Assistant entities**  
- 🛠️ **Extensible by the community**  

---

## 🚧 Current Status

- ✔️ Fully working on **Deye Hybrid** (validated)  
- ✔️ Architecture ready for **multi‑brand support**  
- ⏳ Additional YAML definitions needed for other brands  
- 🤝 Community contributions welcome  

---

[📄 Solarmodbus Documentation (PDF)](./solarmodbus.pdf)

-    How to install on HAOS:

Just past this one-line on you ssh console:

`unzip -o <(curl -fsSL https://github.com/comdif/ha-solarmodbus/archive/refs/heads/main.zip) -d /tmp && cp -r /tmp/ha-solarmodbus-main/solarmodbus /config/custom_components/ && ha core restart`

-    How to install on other OS:

Just copy the solarmodbus directory in your HA custom-component directory.
