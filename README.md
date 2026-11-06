# Industrial Tank Level Monitoring & Process Control Simulator

A Python-based educational simulation of an industrial tank monitoring and control system. The application provides a SCADA-style dashboard for observing tank level, operating a simulated pump and outlet valve, switching between automatic and manual modes, monitoring alarms, and reviewing historical process data.

> **Project scope:** This is a software simulation/prototype. It is not connected to a physical PLC, field instruments, pump, valve, or Siemens PCS 7 / PCS neo / WinCC system. Its interlock is simulated application logic and is not a certified safety instrumented function.

## Features

- SCADA-style Streamlit operator dashboard.
- Automatic mode using a PID-inspired controller to regulate tank level toward an operator setpoint.
- Manual mode allowing the operator to set pump speed.
- Simulated inlet pump and outlet valve.
- Normal, low, high, and high-high level alarm states.
- High-high level pump interlock at a configured threshold of 95%.
- SQLite storage for process history and event logs.
- Historical trend visualization and CSV export.
- Automated unit tests for controller behaviour and database operations.

## Technology stack

| Area | Technology |
|---|---|
| Application / dashboard | Python, Streamlit |
| Visualization | Plotly |
| Historical storage | SQLite |
| Data handling | Pandas |
| Testing | Python `unittest` |

## Project structure

```text
Industrial-Tank-Automation/
├── app.py
├── controller.py
├── database.py
├── industrial_process.db       # Generated/updated when the app runs
├── requirements.txt
├── tests/
│   ├── test_controller.py
│   └── test_database.py
└── documentation/
    ├── project_overview.md
    ├── system_architecture.md
    ├── test_plan.md
    └── test_results.md
```

The virtual environment (`venv/`) should remain local and should not be committed to GitHub.

## Run locally

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Industrial-Tank-Automation
```

### 2. Create and activate a virtual environment

**Windows PowerShell**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
streamlit run app.py
```

Streamlit will provide a local URL, normally `http://localhost:8501`.

## Run automated tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

At the time this documentation was prepared, the controller and database test suites contained **17 automated tests, all passing**.

## Control and alarm behaviour

- **AUTO:** the controller calculates a pump command from the difference between the setpoint and simulated tank level.
- **MANUAL:** the pump command follows the operator-entered manual value.
- **Tank model:** simulated inflow is proportional to pump speed and outflow is proportional to valve opening.
- **High alarm:** level at or above 90%.
- **High-high alarm:** level at or above 95%; the application interlock stops the pump.
- **Low alarm:** level at or below 10%.

The simulation updates in discrete steps when the operator runs the process. It is not a continuously scanned real-time control loop.

## Testing status

- Automated controller tests: passed.
- Automated database tests: passed.
- Manual dashboard/system validation: complete this checklist before describing the project as fully validated. See [`documentation/test_plan.md`](documentation/test_plan.md).
- Engineering documentation: included in the `documentation/` directory.

## Limitations and future enhancements

- Replace the simplified tank equations with a calibrated process model.
- Add sensor-failure and invalid-signal simulation.
- Add controller reset/anti-windup behaviour and configurable PID parameters.
- Add configurable alarm limits and alarm acknowledgement.
- Add timestamped operator actions and richer event classification.
- Integrate with a real PLC/SCADA test environment only with appropriate hardware, engineering review, and safety procedures.

## Author

**Brahmi Matey**  
Final-year Computer Engineering student

## Disclaimer

This project is intended for learning and demonstration. It must not be used to control real industrial equipment or as a substitute for a properly engineered, validated, and certified industrial control or safety system.
