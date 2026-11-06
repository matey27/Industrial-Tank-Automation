# System Architecture

## 1. Architecture summary

The application is organized into three primary layers:

1. **Presentation layer — `app.py`:** Streamlit dashboard, operator inputs, process visualization, alarm display, historical trends, and CSV exports.
2. **Control logic layer — `controller.py`:** tank-state simulation, PID-inspired pump calculation, alarm classification, and high-high interlock function.
3. **Persistence layer — `database.py`:** SQLite initialization, process-history storage, event logging, and retrieval functions.

## 2. High-level data flow

```text
        Operator
           |
           v
  Streamlit Dashboard
        app.py
           |
           v
  Operating Mode Selection
      /             \
     v               v
 AUTO Controller   MANUAL Pump
     \               /
      \             /
       v           v
       Interlock Check
              |
              v
       Tank Process Model
              |
              v
       Updated Tank Level
              |
        +-----+------+
        |            |
        v            v
    Alarm Logic   SQLite Logging
        |            |
        v            v
 Dashboard Status  History / Events
        |            |
        +------v-----+
          Trends / CSV
```

## 3. Controller logic

### 3.1 Automatic control

The controller calculates the error:

```text
error = setpoint - current_level
```

The current implementation uses proportional, integral, and derivative terms:

```text
output = (Kp × error) + (Ki × integral) + (Kd × derivative)
```

Configured gains in the current controller:

| Parameter | Value |
|---|---:|
| Kp | 3.0 |
| Ki | 0.08 |
| Kd | 0.5 |

The integral term is bounded between -500 and 500. The final pump command is clamped between 0 and 100.

This is a simplified discrete PID implementation. It is not tuned for a real process and should not be treated as a production control algorithm.

### 3.2 Tank process model

The simplified process model calculates:

```text
inflow  = pump_speed × 0.08
outflow = valve_opening × 0.05

new_level = current_level + inflow - outflow
```

The resulting tank level is limited to the range 0–100%.

### 3.3 Alarm classification

| Condition | Alarm |
|---|---|
| Level ≥ 95% | HIGH-HIGH LEVEL |
| Level ≥ 90% and below 95% | HIGH LEVEL |
| Level ≤ 10% | LOW LEVEL |
| Otherwise | NORMAL |

### 3.4 High-high interlock

The interlock checks both the current and projected tank level. If either reaches or exceeds 95%, the application stops the simulated inlet pump for that process step.

This is software simulation logic only. It is not a safety-rated interlock and has not undergone a functional safety lifecycle.

## 4. Data persistence

The SQLite database is stored locally in `industrial_process.db`.

The application uses two logical record groups:

- **Process history:** operating level, pump command, valve opening, mode, alarm state, and record time.
- **Event log:** event type, description, severity, and record time.

The dashboard retrieves these records for historical tables, trend charts, and CSV downloads.

## 5. Execution sequence

1. Initialize the database and application session state.
2. Display the current process state and operator controls.
3. Read the selected operating mode and operator inputs.
4. Calculate the automatic pump command or read the manual pump command.
5. Estimate the projected tank level.
6. Evaluate the high-high interlock.
7. Apply the pump and valve values to the tank simulation.
8. Determine the resulting alarm state.
9. Save the process sample and any relevant event transition.
10. Refresh the dashboard and historical views.

## 6. Design limitations

- The simulation is discrete-step rather than a continuously executing control loop.
- The process model is linear and simplified.
- No hardware I/O or industrial protocol is implemented.
- No redundancy, watchdog, fail-safe output state, or safety certification is provided.
- The local SQLite database is suitable for a prototype, not a multi-user industrial historian.
