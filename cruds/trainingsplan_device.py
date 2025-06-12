import sqlite3

DB = "WorkoutBuddy.sqlite"
connection = sqlite3.connect(DB)
cursor = connection.cursor()

#----------------------CRUD-FUNCTIONS FOR TRAININGSPLAN_DEVICE----------------------#

def link_device_to_plan(training_plan_id, device_id):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO TrainingPlan_Device (training_plan_id, device_id)
            VALUES (?, ?)
        """, (training_plan_id, device_id))
        conn.commit()

def unlink_device_from_plan(training_plan_id, device_id):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM TrainingPlan_Device
            WHERE training_plan_id = ? AND device_id = ?
        """, (training_plan_id, device_id))
        conn.commit()
