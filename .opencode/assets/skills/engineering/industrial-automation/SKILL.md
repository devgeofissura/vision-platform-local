---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: industrial-automation
description: Program PLCs (IEC 61131-3) with Structured Text and Ladder, and design HMIs and SCADA for industrial automation.
category: engineering
version: 0.1.0
author: devtiagoabreu
tags: [plc, iec-61131, scada, hmi, automation, opcua, ladder]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - IEC 61131-3 concepts or a PLC IDE (CODESYS, TwinCAT, TIA Portal)
  - Networking fundamentals for fieldbus and OPC UA
  - Basic electrical schematics reading (relays, sensors, 24 V)
provides:
  - Structured Text program patterns
  - Ladder logic translation and patterns
  - HMI and SCADA tag-mapping guidance
  - Safety and fault-handling practices
---

# industrial-automation

## Overview

Industrial automation runs machines and processes with PLCs (Programmable
Logic Controllers) following the IEC 61131-3 standard. The standard
defines five languages: Structured Text (ST), Ladder (LD), Function Block
Diagram (FBD), Instruction List (IL), and Sequential Function Chart (SFC).

PLCs run a cyclic scan: read inputs, execute logic, write outputs.
Anything you design must fit one scan cycle. This skill covers ST and
LD patterns, plus HMI/SCADA integration so operators can monitor and
control the process.

## Prerequisites

- Access to a PLC IDE (CODESYS, TwinCAT, TIA Portal) or an emulator
- Understanding of contacts, coils, and boolean logic
- Basic networking (Ethernet/IP, Modbus TCP, or OPC UA) knowledge
- 24 V DC field wiring concepts (sensors, actuators, PLC I/O cards)

## Usage Instructions

### 1. Structured Text (IEC 61131-3)

Write logic as functions and function blocks with typed variables.
Capture state with `BOOL`/`INT` variables and edge detection rather
than relying on scan order alone.

```iecst
PROGRAM MotorControl
VAR
    Start    : BOOL;
    Stop     : BOOL;
    Run      : BOOL;
    SafetyOK : BOOL;
    RunPrev  : BOOL;
END_VAR

// Safety first: stop dominates start
Run := (Run OR Start) AND NOT Stop AND SafetyOK;
```

### 2. Ladder Logic Patterns

Ladder mirrors relay circuits: series contacts are AND, parallel are OR.
The equivalent of the ST block above, with a latching seal-in:

```text
|  Start    Stop     SafetyOK    Run      |
|--[ ]------[\/]-------[ ]--------( )----|
|  Run                                   |
|--[ ]-----------------------------------|
```

The seal-in (holding) contact keeps the coil energized after Start
releases. Put stop and safety contacts in series so any of them cuts
the output immediately.

### 3. HMI and SCADA Tag Mapping

An HMI shows plant data; SCADA adds logging and supervisory control.
The key discipline is consistent tag naming so the HMI binds to PLC
addresses without hardcoded magic numbers.

```json
{
  "tags": [
    { "name": "LINE1/MOTOR_RUN", "plc": "GVL.Motor.Run", "type": "BOOL", "writable": false },
    { "name": "LINE1/TANK_LEVEL", "plc": "GVL.Level", "type": "REAL", "scale": [0, 10] },
    { "name": "LINE1/ALARM_OVERTEMP", "plc": "GVL.TempAlarm", "type": "BOOL", "priority": "high" }
  ]
}
```

### 4. OPC UA Client Example

For modern integration, read and write PLC tags from a Python SCADA
layer over OPC UA:

```python
from opcua import Client

client = Client("opc.tcp://192.168.0.10:4840")
client.connect()
try:
    node = client.get_node("ns=4;s=GVL.Motor.Run")
    node.set_value(True)
    print("Motor.Run =", node.get_value())
finally:
    client.disconnect()
```

## Best Practices

- Use edge detection for start/stop pushbuttons; a stuck contact must not re-trigger.
- Wire stop/safety inputs normally-closed and use `NOT` in logic, so a wire break fails safe.
- Keep motor control in one function block with local state; never duplicate logic across programs.
- Version-control PLC projects; a change without review can stop a line.
- Name tags consistently (area/device/metric) across PLC, HMI, and SCADA.

## Pitfalls / Common Mistakes

- Forgetting the scan cycle: reading a value you wrote in the same cycle is unreliable.
- Confusing energize-to-stop with de-energize-to-stop, creating unsafe behavior.
- Using timers/delays inside logic that must react within one scan.
- Hardcoding tag addresses in the HMI instead of importing the tag list.
- Ignoring cold/warm start behavior — outputs can latch unexpectedly after a restart.

## Examples

### Example 1: Toggle with edge (ST)

```iecst
VAR Toggle, In, TogglePrev : BOOL; END_VAR
IF In AND NOT TogglePrev THEN
    Toggle := NOT Toggle;
END_IF
TogglePrev := In;
```

### Example 2: Timer-based sequence (ST using a TON block)

```iecst
TON Timer1(IN := Start, PT := T#5S);
ValveOpen := Timer1.Q AND TankLow AND NOT Stop;
```

## References

- [IEC 61131-3 overview](https://en.wikipedia.org/wiki/IEC_61131-3)
- [CODESYS documentation](https://www.codesys.com)
- [python-opcua client](https://python-opcua.readthedocs.io/)
