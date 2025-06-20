import sqlite3

connection = sqlite3.connect('WorkoutBuddy.sqlite')
cursor = connection.cursor()

# ---------------------- CREATE THE DATABASE ---------------------- #

cursor.execute("""
CREATE TABLE IF NOT EXISTS Device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    repetitions INTEGER,
    break_time INTEGER,
    sets INTEGER,
    weight INTEGER,
    picture_path TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS TrainingPlan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message_time INTEGER
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS TrainingPlan_Device (
    training_plan_id INTEGER,
    device_id INTEGER,
    PRIMARY KEY (training_plan_id, device_id),
    FOREIGN KEY (training_plan_id) REFERENCES TrainingPlan(id),
    FOREIGN KEY (device_id) REFERENCES Device(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS TrainingPlan_Weekday (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_plan_id INTEGER,
    weekday TEXT,
    FOREIGN KEY (training_plan_id) REFERENCES TrainingPlan(id)
);
""")


connection.close()