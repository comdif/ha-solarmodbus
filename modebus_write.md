# Solarmodbus Write Script & Lovelace Controls (Deye Hybrid)

This documentation explains how to create a simple Modbus write script in Home Assistant and how to build native Lovelace buttons to toggle the **Solar Sell** mode (`Enabled` / `Disabled`) on Deye Hybrid inverters.

Everything below is **100% Home Assistant native** — no custom cards, no external dependencies.

**Tested and validated on: `deye-SG05LP1-EU-AM2-P`**

---

## ⚠️ Critical Warning — Read Before Using

This method can be used on **any inverter model compatible with Solarman Modbus**, including Deye, SunSynk, LuxPower, and other OEM variants.

However:

### **Writing Modbus registers without full knowledge of your inverter can severely damage the device.**

Incorrect register writes may:

- disable internal protections  
- overload or overstress components  
- corrupt configuration  
- cause unpredictable behavior  
- **permanently break the inverter**

You must:

- know **exactly** which register you are writing  
- know **exactly** which values are valid  
- understand the **impact** of the change  
- verify the register list for **your specific model**

### **I decline all responsibility for any damage caused by using this method on other inverter models, or by modifying register numbers or values beyond the example provided here.**

Use this method **entirely at your own risk**.

---

### Modbus Write Script

Add the following script to your scripts.yaml.
It exposes two fields: address (Modbus register) and value (integer to write).

```
modbuswrite:
  fields:
    address:
      description: Register
    value:
      description: Value
  sequence:
  - data:
      address: '{{ address | int }}'
      value: '{{ value | int }}'
    action: solarmodbus.write_register
  alias: modbuswrite
  description: ''
```
### Lovelace Buttons — Solar Sell Enable/Disable

The following Lovelace card shows only one button at a time, depending on the current inverter state:

If the sensor reports Enabled → show Disable Solar Sell

If the sensor reports Disabled → show Enable Solar Sell

This keeps the UI clean and prevents accidental double actions.
```
type: horizontal-stack
cards:
  - type: conditional
    conditions:
      - entity: sensor.solarmodbus_device_solar_sell
        state: Enabled
    card:
      type: tile
      entity: sensor.solarmodbus_device_solar_sell
      name: Disable Solar Sell
      icon: mdi:block-helper
      tap_action:
        action: call-service
        service: script.modbuswrite
        data:
          address: 247
          value: 0
  - type: conditional
    conditions:
      - entity: sensor.solarmodbus_device_solar_sell
        state: Disabled
    card:
      type: tile
      entity: sensor.solarmodbus_device_solar_sell
      name: Enable Solar Sell
      icon: mdi:solar-power
      tap_action:
        action: call-service
        service: script.modbuswrite
        data:
          address: 247
          value: 1
```
