# Project Overview

## 1. Project title

**Industrial Tank Level Monitoring & Process Control Simulator**

## 2. Purpose

The project simulates a basic industrial tank-level process and demonstrates core automation concepts through a software dashboard. It provides a controlled environment to observe a process variable, adjust an operating setpoint, control a simulated pump and outlet valve, detect abnormal operating conditions, and retain process history.

## 3. Objectives

1. Build a dashboard that presents the tank's operating state in an operator-friendly format.
2. Simulate automatic and manual pump operation.
3. Implement a PID-inspired control calculation for automatic level regulation.
4. Detect low, high, and high-high tank-level conditions.
5. Simulate a high-high interlock that stops the inlet pump.
6. Store process samples and event records in SQLite.
7. Verify controller and database functions using automated tests.

## 4. Scope

The current implementation is a single-tank, discrete-step simulation. The operator interacts with the application through Streamlit controls. The process model calculates changes in tank level from pump speed and outlet-valve opening. The application records process history and events in a local SQLite database.

The project does not include physical sensors, actuators, PLC hardware, industrial communication protocols, or a live connection to Siemens automation software.

## 5. Main functions

| Function | Description |
|---|---|
| Process monitoring | Displays simulated tank level and equipment state |
| AUTO operation | Calculates pump command using setpoint error |
| MANUAL operation | Uses the operator's manual pump command |
| Outlet control | Simulates outflow based on valve opening |
| Alarm monitoring | Identifies low, high, and high-high level states |
| Interlock | Stops the simulated pump when the high-high condition is reached or projected |
| Historical records | Saves process values and events to SQLite |
| Reporting | Displays trends and supports CSV export |

## 6. Operating assumptions

- Tank level is represented as a percentage from 0% to 100%.
- Pump speed and valve opening are represented on a 0–100 scale.
- The simulation advances when the operator activates the process-run control.
- The process equations are simplified and are intended to demonstrate control behaviour, not predict a real tank's hydraulics.
- Alarm thresholds are configured in software and are not derived from a formal hazard analysis.

## 7. Completion status

The working dashboard, controller logic, SQLite logging, and 17 automated tests have been implemented. The automated test run completed successfully with 17/17 tests passing. Manual end-to-end validation and final repository review should be completed before presenting the project as fully validated.
