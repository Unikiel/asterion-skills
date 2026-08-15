# Hardware InnovationLab Workflow

## Contents

1. Required outputs
2. Bill of materials
3. Power and wiring rules
4. Diagram requirements
5. Module bring-up guide
6. Mandatory hardware quick-test pack
7. Integration and validation
8. Architecture freeze and exact-target hardware lock
9. Hardware evidence blocking for automatic sessions

## 1. Required outputs

For every hardware-involved project provide:

- approved bill of materials with exact model/SKU where known;
- one coherent power architecture;
- physical placement and enclosure/environment notes;
- wiring architecture diagram in English by default;
- separate system concept/logic diagram in English by default;
- step-by-step first-connection guide for every controller, interface board,
  sensor, probe, switch, actuator, display, communication module, and supply;
- a mandatory hardware quick-test pack containing isolated tests for every
  controller and approved module, staged subsystem tests, and a complete
  integration test;
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

## 6. Mandatory hardware quick-test pack

Every hardware-involved project must include a self-contained quick-test pack.
It is a release requirement, not an optional appendix. Organize it so a student
can verify hardware safely before relying on the full application.

### 6.1 Required structure

Provide these layers in order:

1. **Controller baseline tests:** one test per controller covering power, USB or
   programming connection, exact board selection, upload, reset behavior, and
   serial output.
2. **Separated module tests:** one isolated test for every approved sensor,
   actuator, switch, display, interface board, communication module, and power
   stage connected only to its owning controller and minimum required support
   circuit.
3. **Subsystem tests:** combine only modules that share one bus, power domain,
   controller, or tightly coupled function; verify addresses, timing, resource
   conflicts, and power margin.
4. **Integration test:** connect the frozen complete architecture and verify the
   end-to-end hardware route, controller-to-controller communication, data
   flow, actuation, alarms, safe state, restart, and recovery as applicable.

For multi-controller projects, keep controller-specific separated tests in
distinct folders and include controller-to-controller communication as a
separate subsystem gate before complete integration.

### 6.2 Required content for every quick test

Each test must state:

- test ID, exact model/SKU, owning controller, and purpose;
- prerequisites and required tools;
- exact pin-to-pin wiring and power source;
- locked IDE/framework, board target, libraries, and relevant versions;
- minimal standalone firmware or an equally precise test procedure;
- upload/run steps and serial-monitor settings where applicable;
- expected serial, electrical, visual, mechanical, or network result;
- explicit pass/fail criteria and evidence to save;
- diagnosis order for common failures;
- safe disconnect, rollback, and next permitted test.

Use real runnable tests rather than pseudocode or placeholder sketches. Keep
each separated test independent of the dashboard, cloud service, database, and
unrelated modules unless that dependency is the subject of the test.

### 6.3 Mandatory gates

- Run controller baseline tests before module tests.
- Do not mark a separated test passed without required physical evidence.
- Do not begin a subsystem test until all participating separated tests pass.
- Do not begin the complete integration test until every required separated and
  subsystem test passes.
- If integration fails, return to the last passing isolated/subsystem
  configuration; do not rewrite or discard earlier evidence.
- Record each result, evidence path, blocker, and next action in `TASKS.md` and
  the project evidence structure.
- Distinguish `NOT_RUN`, `BLOCKED`, `FAILED`, and `PASSED`; never translate file
  presence, compilation, mocks, or simulated readings into physical success.

The project plan and session prompts must allocate explicit time for separated
tests and integration testing. Hardware contingency hours do not replace these
planned validation sessions.

## 7. Integration and validation

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

## 8. Architecture Freeze and Exact-Target Hardware Lock

This section extends, and does not replace, Sections 1–6 above.

Before generating wiring, firmware, session prompts, or starter code:

1. enumerate every controller and exact controller model;
2. assign every sensor, actuator, interface board, communication module, and
   power domain to its owning controller;
3. distinguish shared buses from physically independent buses;
4. freeze controller-to-controller/network topology and the data aggregation
   point;
5. freeze the firmware platform: IDE/framework, board package/core, board/FQBN
   or compile target, and relevant library constraints;
6. freeze pins, bus addresses, reserved pins, boot/strapping constraints, USB
   behavior, and power boundaries;
7. record deprecated topology assumptions so that legacy single-controller or
   generic-family examples cannot leak into the new package.

For every multi-controller project additionally produce:

- `Controller_Inventory`;
- `Sensor_Ownership_Matrix`;
- `Firmware_Platform_Lock`;
- wiring architecture consistent with that ownership;
- a system concept diagram consistent with the same topology.

### Exact-target rule

Do not treat a generic MCU family example as sufficient evidence for a concrete
target. For example, ESP32-C3 must not be silently treated as generic ESP32.
Board-specific APIs, USB/serial behavior, reserved pins, boot constraints, and
compile target must be checked for the locked board.

When a compiler/toolchain is available, compile the generated firmware for the
locked target before packaging. If that cannot be run, state the limitation
explicitly rather than claiming target compatibility.

## 9. Hardware Evidence Blocking for Automatic Sessions

Automatic BigBang orchestration may prepare and validate software-side checks,
but it must not auto-pass a physical gate.

A hardware session remains `BLOCKED` or `VERIFYING` until the required physical
evidence exists, such as:

- serial output;
- measured voltage/current;
- sensor reading;
- photo of wiring/placement;
- continuity or logic-level observation;
- student/teacher manual acceptance record.

The state system must preserve the active session and resume checkpoint instead
of advancing automatically.
