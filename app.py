
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime
from controller import TankController, high_high_interlock

from database import (
    initialize_database,
    save_process_record,
    save_event,
    get_process_history,
    get_event_history
)


# ----------------------------------
# 1. PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Industrial SCADA System",
    page_icon="🏭",
    layout="wide"
)

# Initialize SQLite database
initialize_database()


# ----------------------------------
# 2. SESSION STATE
# ----------------------------------

if "controller" not in st.session_state:
    st.session_state.controller = TankController()

if "last_pump" not in st.session_state:
    st.session_state.last_pump = 0.0

if "last_valve" not in st.session_state:
    st.session_state.last_valve = 25.0

if "last_alarm" not in st.session_state:
    st.session_state.last_alarm = (
        st.session_state.controller.get_alarm()
    )

controller = st.session_state.controller


# ----------------------------------
# 3. DASHBOARD HEADER
# ----------------------------------

st.title("INDUSTRIAL PROCESS CONTROL SYSTEM")

st.caption(
    "Tank Level Monitoring | Process Automation | SCADA Simulation"
)

st.divider()


# ----------------------------------
# 4. SIDEBAR CONTROLS
# ----------------------------------

st.sidebar.title("OPERATOR PANEL")

mode = st.sidebar.radio(
    "Operating Mode",
    ["AUTO", "MANUAL"]
)

setpoint = st.sidebar.slider(
    "Tank Level Setpoint (%)",
    10,
    90,
    60
)

valve_opening = st.sidebar.slider(
    "Outlet Valve Opening (%)",
    0,
    100,
    25
)

if mode == "MANUAL":

    manual_pump = st.sidebar.slider(
        "Pump Speed (%)",
        0,
        100,
        50
    )

else:
    manual_pump = 0


run = st.sidebar.button(
    "RUN PROCESS",
    type="primary",
    use_container_width=True
)

reset = st.sidebar.button(
    "RESET SYSTEM",
    use_container_width=True
)


# ----------------------------------
# 5. RESET SYSTEM
# ----------------------------------

if reset:

    st.session_state.controller = TankController()

    st.session_state.last_pump = 0.0
    st.session_state.last_valve = 25.0
    st.session_state.last_alarm = "NORMAL"

    save_event(
        event_type="SYSTEM",
        description="Process simulation was reset",
        severity="INFO"
    )

    st.rerun()


# ----------------------------------
# 6. PROCESS EXECUTION
# ----------------------------------

if run:

    # Capture previous alarm before updating the process
    previous_alarm = st.session_state.last_alarm

    # Determine pump speed
    if mode == "AUTO":

        pump_speed = controller.calculate_pid(setpoint)

    else:

        pump_speed = float(manual_pump)

    # Predict next tank level
    projected_level = (
        controller.level
        + pump_speed * 0.08
        - valve_opening * 0.05
    )

    # High-high level interlock
    interlock_activated = high_high_interlock(
    current_level=controller.level,
    projected_level=projected_level
)

    if interlock_activated:

        pump_speed = 0.0

        save_event(
            event_type="INTERLOCK",
            description=(
                "High-high level interlock activated. "
                "Pump automatically stopped."
            ),
            severity="CRITICAL"
        )

    # Update tank process
    level = controller.update_tank(
        pump_speed,
        valve_opening
    )

    # Determine current alarm
    alarm = controller.get_alarm()

    # Update equipment states
    st.session_state.last_pump = pump_speed
    st.session_state.last_valve = valve_opening

    # ----------------------------------
    # SAVE PROCESS DATA TO SQLITE
    # ----------------------------------

    save_process_record(
        level=round(level, 2),
        pump=round(pump_speed, 2),
        valve=round(valve_opening, 2),
        mode=mode,
        alarm=alarm
    )

    # ----------------------------------
    # SAVE ALARM TRANSITIONS
    # ----------------------------------

    if alarm != previous_alarm:

        save_event(
            event_type="ALARM",
            description=(
                f"Alarm changed from {previous_alarm} to {alarm}"
            ),
            severity=(
                "WARNING" if alarm != "NORMAL" else "INFO"
            )
        )

    # Save latest alarm state
    st.session_state.last_alarm = alarm

    # ----------------------------------
    # SAVE PROCESS EXECUTION EVENT
    # ----------------------------------

    save_event(
        event_type="PROCESS",
        description=f"Process executed in {mode} mode",
        severity="INFO"
    )


# ----------------------------------
# 7. CURRENT PROCESS VALUES
# ----------------------------------

level = controller.level

pump = st.session_state.last_pump

valve = st.session_state.last_valve

alarm = controller.get_alarm()

pump_status = "ON" if pump > 0 else "OFF"

valve_status = "OPEN" if valve > 0 else "CLOSED"


# ----------------------------------
# 8. SYSTEM STATUS
# ----------------------------------

st.subheader("SYSTEM STATUS")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Tank Level",
    f"{level:.1f}%"
)

c2.metric(
    "Pump Status",
    pump_status
)

c3.metric(
    "Valve Status",
    valve_status
)

c4.metric(
    "Operating Mode",
    mode
)


# ----------------------------------
# 9. ALARM PANEL
# ----------------------------------

st.subheader("ALARM MONITORING")

if alarm == "NORMAL":

    st.success("SYSTEM NORMAL")

elif alarm == "HIGH LEVEL":

    st.warning("HIGH LEVEL ALARM")

elif alarm == "HIGH-HIGH LEVEL":

    st.error("HIGH-HIGH LEVEL - PUMP INTERLOCK")

elif alarm == "LOW LEVEL":

    st.error("LOW LEVEL ALARM")

else:

    st.info(alarm)


st.divider()


# ----------------------------------
# 10. GRAPHICAL TANK
# ----------------------------------

st.subheader("LIVE PROCESS VISUALIZATION")

col1, col2 = st.columns([1, 1])

with col1:

    tank_fig = go.Figure()

    # Water inside the tank
    tank_fig.add_shape(
        type="rect",
        x0=3,
        x1=7,
        y0=5,
        y1=5 + (level * 0.9),
        fillcolor="#3498DB",
        line=dict(width=0)
    )

    # Tank outline
    tank_fig.add_shape(
        type="rect",
        x0=3,
        x1=7,
        y0=5,
        y1=95,
        fillcolor="rgba(0,0,0,0)",
        line=dict(color="#34495E", width=4)
    )

    tank_fig.add_annotation(
        x=5,
        y=50,
        text=f"<b>{level:.1f}%</b>",
        showarrow=False,
        font=dict(size=24, color="white")
    )

    tank_fig.add_annotation(
        x=5,
        y=100,
        text="STORAGE TANK",
        showarrow=False,
        font=dict(size=16)
    )

    tank_fig.update_layout(
        height=400,
        xaxis=dict(
            range=[0, 10],
            visible=False
        ),
        yaxis=dict(
            range=[0, 110],
            visible=False
        ),
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False
    )

    st.plotly_chart(
        tank_fig,
        use_container_width=True
    )


with col2:

    st.markdown("### EQUIPMENT STATUS")

    if pump_status == "ON":

        st.success("PUMP: RUNNING")

    else:

        st.error("PUMP: STOPPED")

    st.write(f"Pump speed: {pump:.1f}%")

    st.divider()

    if valve_status == "OPEN":

        st.success("OUTLET VALVE: OPEN")

    else:

        st.warning("OUTLET VALVE: CLOSED")

    st.write(f"Valve opening: {valve:.1f}%")

    st.divider()

    st.info(
        f"Level transmitter reading: {level:.2f}%"
    )

    st.info(
        f"Controller setpoint: {setpoint}%"
    )


# ----------------------------------
# 11. PROCESS FLOW DIAGRAM
# ----------------------------------

st.subheader("PROCESS FLOW DIAGRAM")

flow_fig = go.Figure()

# Water supply pipe
flow_fig.add_shape(
    type="line",
    x0=0.5,
    y0=3,
    x1=3,
    y1=3,
    line=dict(color="#3498DB", width=5)
)

# Pump
pump_color = "#16A36A" if pump > 0 else "#C0392B"

flow_fig.add_shape(
    type="circle",
    x0=2.5,
    x1=3.5,
    y0=2.5,
    y1=3.5,
    fillcolor=pump_color,
    line=dict(color=pump_color)
)

flow_fig.add_annotation(
    x=3,
    y=3,
    text="P",
    showarrow=False,
    font=dict(color="white", size=18)
)

flow_fig.add_annotation(
    x=3,
    y=2.1,
    text="PUMP",
    showarrow=False
)

# Pipe from pump to tank
flow_fig.add_shape(
    type="line",
    x0=3.5,
    y0=3,
    x1=6,
    y1=3,
    line=dict(color="#3498DB", width=5)
)

# Tank
flow_fig.add_shape(
    type="rect",
    x0=6,
    x1=8,
    y0=2,
    y1=4,
    fillcolor="rgba(52,152,219,0.25)",
    line=dict(color="#34495E", width=3)
)

flow_fig.add_annotation(
    x=7,
    y=3,
    text=f"TANK<br>{level:.1f}%",
    showarrow=False,
    font=dict(size=16)
)

# Outlet pipe
flow_fig.add_shape(
    type="line",
    x0=8,
    y0=3,
    x1=9.5,
    y1=3,
    line=dict(color="#3498DB", width=5)
)

# Valve
valve_color = "#16A36A" if valve > 0 else "#C0392B"

flow_fig.add_shape(
    type="path",
    path="M 8.7,2.7 L 9.0,3 L 8.7,3.3 Z",
    fillcolor=valve_color,
    line=dict(color=valve_color)
)

flow_fig.add_shape(
    type="path",
    path="M 9.3,2.7 L 9.0,3 L 9.3,3.3 Z",
    fillcolor=valve_color,
    line=dict(color=valve_color)
)

flow_fig.add_annotation(
    x=9,
    y=2.1,
    text="OUTLET VALVE",
    showarrow=False
)

flow_fig.update_layout(
    height=300,
    xaxis=dict(
        range=[0, 10],
        visible=False
    ),
    yaxis=dict(
        range=[1, 5],
        visible=False
    ),
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10)
)

st.plotly_chart(
    flow_fig,
    use_container_width=True
)


# ----------------------------------
# 12. HISTORICAL PROCESS TREND
# ----------------------------------

st.divider()

st.subheader("PROCESS TREND ANALYSIS")

# Retrieve data from SQLite
process_df = get_process_history()

if not process_df.empty:

    # Display oldest to newest in the trend
    process_df = process_df.sort_values("id")

    trend_fig = go.Figure()

    trend_fig.add_trace(
        go.Scatter(
            x=process_df["id"],
            y=process_df["tank_level"],
            mode="lines+markers",
            name="Tank Level"
        )
    )

    trend_fig.add_hline(
        y=setpoint,
        line_dash="dash",
        annotation_text="Current Setpoint"
    )

    trend_fig.update_layout(
        xaxis_title="Process Record",
        yaxis_title="Tank Level (%)",
        yaxis=dict(range=[0, 100]),
        height=350
    )

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    st.markdown("### HISTORICAL PROCESS RECORDS")

    st.dataframe(
        process_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = process_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="DOWNLOAD PROCESS HISTORY",
        data=csv_data,
        file_name="industrial_process_history.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Execute the process to generate historical data."
    )


# ----------------------------------
# 13. ALARM AND EVENT HISTORY
# ----------------------------------

st.divider()

st.subheader("ALARM AND EVENT HISTORY")

event_df = get_event_history()

if not event_df.empty:

    st.dataframe(
        event_df,
        use_container_width=True,
        hide_index=True
    )

    event_csv = event_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="DOWNLOAD EVENT HISTORY",
        data=event_csv,
        file_name="industrial_event_history.csv",
        mime="text/csv"
    )

else:

    st.info("No process events recorded yet.")


# ----------------------------------
# 14. FOOTER
# ----------------------------------

st.divider()

st.caption(
    "Industrial Tank Automation Simulator | "
    "Educational Demonstration | "
    "Python + Streamlit + Plotly + SQLite"
)
