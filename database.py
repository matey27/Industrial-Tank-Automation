import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "industrial_process.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Stores every process execution
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS process_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            tank_level REAL,
            pump_speed REAL,
            valve_opening REAL,
            operating_mode TEXT,
            alarm_status TEXT
        )
    """)

    # Stores alarm and equipment events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            description TEXT,
            severity TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_process_record(level, pump, valve, mode, alarm):
    conn = get_connection()

    conn.execute("""
        INSERT INTO process_history
        (timestamp, tank_level, pump_speed, valve_opening,
         operating_mode, alarm_status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        level,
        pump,
        valve,
        mode,
        alarm
    ))

    conn.commit()
    conn.close()


def save_event(event_type, description, severity="INFO"):
    conn = get_connection()

    conn.execute("""
        INSERT INTO event_log
        (timestamp, event_type, description, severity)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        event_type,
        description,
        severity
    ))

    conn.commit()
    conn.close()


def get_process_history():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM process_history ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def get_event_history():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM event_log ORDER BY id DESC",
        conn
    )
    conn.close()
    return df