import sqlite3

connection = sqlite3.connect('WorkoutBuddy.sqlite')
cursor = connection.cursor()

# ---------------------- CREATE THE DATABASE ---------------------- #

# Devices table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    active_time INTEGER,
    break_time INTEGER,
    sets INTEGER,
    picture_path TEXT
);
""")

# Training plans table
cursor.execute("""
CREATE TABLE IF NOT EXISTS TrainingPlan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message_time INTEGER
);
""")

# Many-to-many relationship: training plans and devices
cursor.execute("""
CREATE TABLE IF NOT EXISTS TrainingPlan_Device (
    training_plan_id INTEGER,
    device_id INTEGER,
    PRIMARY KEY (training_plan_id, device_id),
    FOREIGN KEY (training_plan_id) REFERENCES TrainingPlan(id),
    FOREIGN KEY (device_id) REFERENCES Device(id)
);
""")

# Training days for each plan
cursor.execute("""
CREATE TABLE IF NOT EXISTS TrainingPlan_Weekday (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_plan_id INTEGER,
    weekday TEXT,
    FOREIGN KEY (training_plan_id) REFERENCES TrainingPlan(id)
);
""")

connection.close()