import sqlite3

DB = "WorkoutBuddy.sqlite"
connection = sqlite3.connect(DB)
cursor = connection.cursor()

#---------------------- CREATE TRAININGPLAN_WEEKDAY ----------------------#
def add_weekday_to_plan(training_plan_id, weekday):
    cursor.execute("""
        INSERT INTO TrainingPlan_Weekday (training_plan_id, weekday)
        VALUES (?, ?)
        """, 
        (training_plan_id, weekday))
    connection.commit()

#---------------------- READ TRAININGPLAN_WEEKDAY ----------------------#
def get_weekdays_for_plan(training_plan_id):
    cursor.execute("""
        SELECT weekday FROM TrainingPlan_Weekday
        WHERE training_plan_id = ?
    """, 
    (training_plan_id,))
    return [row[0] for row in cursor.fetchall()]

#---------------------- UPDATE TRAININGPLAN_WEEKDAY ----------------------#
#TODO

#---------------------- DELETE TRAININGPLAN_WEEKDAY ----------------------#
def remove_weekday_from_plan(training_plan_id, weekday):
    cursor.execute("""
        DELETE FROM TrainingPlan_Weekday
        WHERE training_plan_id = ? AND weekday = ?
        """, 
        (training_plan_id, weekday))
    connection.commit()
