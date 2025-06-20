import sqlite3

DB = "WorkoutBuddy.sqlite"
connection = sqlite3.connect(DB)
cursor = connection.cursor()

#---------------------- CREATE TRAININGSPLAN ----------------------#
def create_training_plan(name, message_time):
    cursor.execute("""
        INSERT INTO TrainingPlan (name, message_time)
        VALUES (?, ?)
        """, 
        (name, message_time))
    connection.commit()

#---------------------- READ TRAININGSPLAN ----------------------#
def read_all_training_plans():
    cursor.execute("SELECT * FROM TrainingPlan")
    return cursor.fetchall()

#---------------------- UPDATE TRAININGSPLAN ----------------------#
def update_training_plan(plan_id, name, message_time):
    cursor.execute("""
        UPDATE TrainingPlan
        SET name = ?, message_time = ?
        WHERE id = ?
        """, 
        (name, message_time, plan_id))
    connection.commit()

#---------------------- DELETE TRAININGSPLAN ----------------------#
def delete_training_plan(plan_id):
    cursor.execute("DELETE FROM TrainingPlan WHERE id = ?", (plan_id,))
    connection.commit()