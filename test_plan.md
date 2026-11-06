# Test Plan and Validation Checklist

## 1. Purpose

This document defines the tests used to verify the tank controller, interlock, database functions, and dashboard-level operating behaviour.

## 2. Automated unit tests

Automated tests are run from the project root:

```bash
python -m unittest discover -s tests -v
```

### Controller tests

| ID | Test | Expected result |
|---|---|---|
| CT-01 | Initial tank level | Controller initializes at 35% |
| CT-02 | Pump inflow | Tank level increases when pump is operated |
| CT-03 | Outlet flow | Tank level decreases when outlet is open |
| CT-04 | Upper bound | Tank level does not exceed 100% |
| CT-05 | Lower bound | Tank level does not fall below 0% |
| CT-06 | Normal alarm | Normal range returns `NORMAL` |
| CT-07 | High alarm | Level at 90% returns `HIGH LEVEL` |
| CT-08 | High-high alarm | Level at 95% returns `HIGH-HIGH LEVEL` |
| CT-09 | Low alarm | Level at 10% returns `LOW LEVEL` |
| CT-10 | PID output bounds | Pump command remains between 0 and 100 |
| CT-11 | Current-level interlock | Interlock activates at the threshold |
| CT-12 | Projected-level interlock | Interlock activates if projected level reaches threshold |
| CT-13 | Below-threshold interlock | Interlock remains inactive below threshold |

### Database tests

| ID | Test | Expected result |
|---|---|---|
| DB-01 | Database initialization | Database and required tables are created |
| DB-02 | Process record insertion | Process record is stored |
| DB-03 | Event insertion | Event record is stored |
| DB-04 | Multiple process records | Multiple records can be stored and retrieved |

## 3. Automated test result

The last recorded automated run reported:

```text
Ran 17 tests
OK
```

Result: **17 of 17 automated tests passed.**

## 4. Manual system validation checklist

Complete these checks in the running Streamlit application. Record the actual observed result and date in the test-results document.

| ID | Procedure | Expected result | Status |
|---|---|---|---|
| SYS-01 | Select AUTO, choose a setpoint above current level, and run a process step | Controller requests pump operation to raise level | Pending manual verification |
| SYS-02 | Select MANUAL, set a non-zero pump command, and run a process step | Pump command follows the manual setting, unless interlock is active | Pending manual verification |
| SYS-03 | Set outlet valve to 0 and run a step with pump at 0 | Level does not decrease due to outlet flow | Pending manual verification |
| SYS-04 | In a controlled test state, set level to 90% and inspect alarm | HIGH LEVEL is displayed | Pending manual verification |
| SYS-05 | In a controlled test state, reach 95% or projected 95% | HIGH-HIGH alarm appears and pump is stopped | Pending manual verification |
| SYS-06 | In a controlled test state, set level to 10% | LOW LEVEL is displayed | Pending manual verification |
| SYS-07 | Save records, restart the app, and inspect history | Previously saved database records remain available | Pending manual verification |
| SYS-08 | Use RESET SYSTEM and inspect history | Simulation state resets; historical database records remain | Pending manual verification |

**Important:** Do not modify the live application database or production code just to force alarm thresholds. If the dashboard does not provide a safe way to set a test level, use a separate test fixture or a dedicated test-only script. Never connect this simulation to physical equipment.

## 5. Defect recording

For any failed test, record:
- Test ID
- Steps to reproduce
- Expected result
- Actual result
- Screenshot or relevant terminal output
- Corrective action
- Retest result

## 6. Acceptance criteria

The prototype can be considered validated for demonstration when:
- All automated tests pass.
- All applicable manual checks are executed and recorded.
- No blocking dashboard errors remain.
- Database persistence and reset behaviour are confirmed.
- Known limitations are clearly disclosed.
