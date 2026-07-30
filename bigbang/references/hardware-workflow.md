# Hardware InnovationLab Workflow

## Contents

1. Required outputs
2. Bill of materials
3. Power and wiring rules
4. Diagram requirements
5. Module bring-up guide
6. Integration and validation

## 1. Required outputs

For every hardware-involved project provide:

- approved bill of materials with exact model/SKU where known;
- one coherent power architecture;
- physical placement and enclosure/environment notes;
- wiring architecture diagram in English by default;
- separate system concept/logic diagram in English by default;
- step-by-step first-connection guide for every controller, interface board,
  sensor, probe, switch, actuator, display, communication module, and supply;
- dry-run path that works before all hardware arrives when feasible;
- staged integration, calibration, fault injection, safety, and recovery plan;
- four independent contingency class hours.

## 2. Bill of materials

For every item record:

- exact name, model/SKU, quantity, purpose, acceptable substitute;
- voltage/current requirements and logic level;
- interface and signal type;
- connector, cable, pull-up, level-shifter, driver, protection, and mounting
  needs;
- wet-zone/dry-zone rating and placement;
- expected operating range, accuracy, calibration, and failure behavior;
- source/availability and cost when requested.

Do not approve electrically incompatible modules merely because product pages
claim generic ESP32 compatibility.

## 3. Power and wiring rules

- Design one main adapter architecture unless the hardware genuinely requires
  isolation or separate supplies.
- Show how regulated 5 V and 3.3 V rails derive from that architecture.
- Show shared ground explicitly where required.
- Calculate current budget with startup/stall margin.
- Never power high-current actuators from a controller's logic pin or imply that
  a GPIO supplies motor/servo/load power.
- Specify GPIO, bus address, ADC constraints, PWM capability, pull-ups, driver
  boards, flyback protection, fusing, and level shifting.
- Separate wet probes/switches physically and visually from dry interface
  boards, controllers, connectors, and mains/adapter components.
- State USB-power versus external-power rules and prevent backfeeding.
- Check boot-strapping pins and board-specific reserved pins.

## 4. Diagram requirements

Produce two separate, polished diagrams in English by default. Use another
language only when the user explicitly requests it:

### Wiring architecture diagram

Show:

- actual controller and module models;
- pin-to-pin connections and connector names;
- adapter, regulators, 5 V rail, 3.3 V rail, and shared GND;
- actuator power separately from control signals;
- physical device/tank/enclosure placement;
- wet zone and dry zone boundaries;
- probe/switch placement in the real environment;
- interface boards between probes/loads and controller;
- labels that do not overlap lines or boxes.

The wiring diagram must be physically buildable, not an abstract block diagram.

### System concept/logic diagram

Show sensing/input, validation/state logic, processing, decision, actuation,
display/dashboard, storage/communication, alarms, and fallback states as
applicable. Keep this diagram conceptually separate from wiring.

Do not use labels such as “beginner,” “beginner-friendly,” “for beginners,”
“foolproof,” or equivalent ability labels.

## 5. Module bring-up guide

Write one guide per approved item at the granularity of a first ESP32 laptop
connection. Include:

1. exact model/SKU and purpose;
2. required parts, cables, tools, and software;
3. physical placement and wet/dry restrictions;
4. voltage, current, logic level, and signal type;
5. complete pin-by-pin wiring table;
6. board/driver/library installation with version notes;
7. smallest isolated test firmware or procedure;
8. upload/run instructions;
9. expected serial, visual, electrical, or mechanical result;
10. safe measurement points and expected readings;
11. calibration procedure where applicable;
12. common failure symptoms, diagnosis order, and corrective action;
13. disconnect and power-down procedure;
14. evidence to save before integration.

Never begin full-system wiring before every module passes its isolated gate.

## 6. Integration and validation

Integrate in increasing risk order:

1. controller and serial communication;
2. low-risk digital input/output;
3. buses and sensors;
4. displays and communications;
5. interface/driver boards;
6. externally powered actuators;
7. wet-zone components;
8. full enclosure and sustained test.

At each step verify power rails before connecting signal wires, run a minimal
test, save evidence, and preserve a rollback configuration. Test sensor
disconnection, invalid readings, network loss, restart, actuator stall,
over-current protection, and safe-state behavior as applicable.

Provide a software simulator or mocked input path for early sessions when
possible, but clearly distinguish simulated validation from physical validation.
