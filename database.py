import mysql.connector
from mysql.connector import Error
import datetime

# Database Configuration - UPDATE THESE IF NEEDED
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rune',  # Default for many local setups
    'database': 'os_monitor'
}

def get_connection():
    """Create a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error accessing MySQL: {e}")
        return None

def init_db():
    """Initialize the database and table."""
    conn = get_connection()
    if not conn:
        # Try connecting without database to create it
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database')
        try:
            conn = mysql.connector.connect(**temp_config)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            print("Database created or already exists.")
            conn.close()
            conn = get_connection()
        except Error as e:
            print(f"Critical Error: Could not create database. {e}")
            return

    if conn:
        cursor = conn.cursor()
        # Create metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage FLOAT,
                ram_usage FLOAT,
                disk_usage FLOAT,
                process_count INT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Table 'system_metrics' ready.")

def insert_metric(cpu, ram, disk, processes):
    """Insert a new system metric record."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO system_metrics (cpu_usage, ram_usage, disk_usage, process_count) VALUES (%s, %s, %s, %s)"
        val = (cpu, ram, disk, processes)
        cursor.execute(sql, val)
        conn.commit()
        
        # Cleanup old records (keep last 1000)
        cursor.execute("DELETE FROM system_metrics WHERE id NOT IN (SELECT id FROM (SELECT id FROM system_metrics ORDER BY id DESC LIMIT 1000) x)")
        conn.commit()
        
        cursor.close()
        conn.close()

def fetch_latest():
    """Fetch the most recent metric."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM system_metrics ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    return None

def fetch_history(limit=20):
    """Fetch the last N metrics for charts."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM system_metrics ORDER BY id DESC LIMIT {limit}")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result[::-1] # Reverse to show oldest to newest
    return []
