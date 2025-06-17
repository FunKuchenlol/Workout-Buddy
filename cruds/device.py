import sqlite3

DB = "WorkoutBuddy.sqlite"
connection = sqlite3.connect(DB, check_same_thread=False)
cursor = connection.cursor()

#---------------------- CREATE DEVICE----------------------#
def create_device(name, active_time, break_time, sets, picture_path):
    cursor.execute("""
        INSERT INTO Device (name, active_time, break_time, sets, picture_path)
        VALUES (?, ?, ?, ?, ?)
        """, 
        (name, active_time, break_time, sets, picture_path))
    connection.commit()

#---------------------- READ DEVICE----------------------#
def read_all_devices():
    cursor.execute("SELECT * FROM Device")
    return cursor.fetchall()

#---------------------- UPDATE DEVICE----------------------#
def update_device(device_id, name, active_time, break_time, sets, picture_path):
    cursor.execute("""
        UPDATE Device
        SET name = ?, active_time = ?, break_time = ?, sets = ?, picture_path = ?
        WHERE id = ?
        """, 
        (name, active_time, break_time, sets, picture_path, device_id))
    connection.commit()

#---------------------- DELETE DEVICE----------------------#
def delete_device(device_id):
    cursor.execute("DELETE FROM Device WHERE id = ?", (device_id,))
    connection.commit()