import sqlite3

connection = sqlite3.connect('WorkoutBuddy.sqlite')

cursor = connection.cursor()

#----------------------CREATE THE NESSESARY TABLES----------------------#

cursor.execute("""
               CREATE TABLE IF NOT EXISTS Device (
               ID INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT, 
               activetime INTEGER, 
               breaktime INTEGER, 
               \"set\" INTEGER
               );
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS Trainingsplan (
               ID INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT, 
               weekday1 TEXT, 
               weekday2 TEXT, 
               weekday3 TEXT, 
               message_time INTEGER
               );
               """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Trainingsplan_Device (
               TrainingsplanID INTEGER, 
               DeviceID INTEGER, 
               PRIMARY KEY(TrainingsplanID,DeviceID)
               )
               """)

#----------------------CRUD-FUNCTIONS FOR DEVICE----------------------#

def create_geraet(name, activetime, breaktime, sets):
    cursor.execute("""
        INSERT INTO Geräte (name, activetime, breaktime, "set")
        VALUES (?, ?, ?, ?)
    """, (name, activetime, breaktime, sets))
    connection.commit()

def read_geraete():
    cursor.execute("SELECT * FROM Geräte")
    return cursor.fetchall()

def update_geraet(geraet_id, name=None, activetime=None, breaktime=None, sets=None):
    # Nur die übergebenen Werte werden aktualisiert
    updates = []
    params = []
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if activetime is not None:
        updates.append("activetime = ?")
        params.append(activetime)
    if breaktime is not None:
        updates.append("breaktime = ?")
        params.append(breaktime)
    if sets is not None:
        updates.append('"set" = ?')
        params.append(sets)
    params.append(geraet_id)
    cursor.execute(f"UPDATE Geräte SET {', '.join(updates)} WHERE ID = ?", params)
    connection.commit()

def delete_geraet(geraet_id):
    cursor.execute("DELETE FROM Geräte WHERE ID = ?", (geraet_id,))
    connection.commit()

#----------------------CRUD-FUNCTIONS FOR TRAININGSPLAN----------------------#

def create_trainingsplan(name, weekday1, weekday2, weekday3, message_time):
    cursor.execute("""
        INSERT INTO Trainingsplan (name, weekday1, weekday2, weekday3, message_time)
        VALUES (?, ?, ?, ?, ?)
    """, (name, weekday1, weekday2, weekday3, message_time))
    connection.commit()

def read_trainingsplaene():
    cursor.execute("SELECT * FROM Trainingsplan")
    return cursor.fetchall()

def update_trainingsplan(plan_id, name=None, weekday1=None, weekday2=None, weekday3=None, message_time=None):
    updates = []
    params = []
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if weekday1 is not None:
        updates.append("weekday1 = ?")
        params.append(weekday1)
    if weekday2 is not None:
        updates.append("weekday2 = ?")
        params.append(weekday2)
    if weekday3 is not None:
        updates.append("weekday3 = ?")
        params.append(weekday3)
    if message_time is not None:
        updates.append("message_time = ?")
        params.append(message_time)
    params.append(plan_id)
    cursor.execute(f"UPDATE Trainingsplan SET {', '.join(updates)} WHERE ID = ?", params)
    connection.commit()

def delete_trainingsplan(plan_id):
    cursor.execute("DELETE FROM Trainingsplan WHERE ID = ?", (plan_id,))
    connection.commit()

#----------------------CRUD-FUNCTIONS FOR TRAININGSPLAN_DEVICE----------------------#

def add_device_to_trainingsplan(trainingsplan_id, device_id):
    cursor.execute("""
        INSERT INTO Trainingsplan_Device (TrainingsplanID, DeviceID)
        VALUES (?, ?)
    """, (trainingsplan_id, device_id))
    connection.commit()

def remove_device_from_trainingsplan(trainingsplan_id, device_id):
    cursor.execute("""
        DELETE FROM Trainingsplan_Device
        WHERE TrainingsplanID = ? AND DeviceID = ?
    """, (trainingsplan_id, device_id))
    connection.commit()

def get_devices_for_trainingsplan(trainingsplan_id):
    cursor.execute("""
        SELECT Device.*
        FROM Device
        JOIN Trainingsplan_Device ON Device.ID = Trainingsplan_Device.DeviceID
        WHERE Trainingsplan_Device.TrainingsplanID = ?
    """, (trainingsplan_id,))
    return cursor.fetchall()

def get_trainingsplaene_for_device(device_id):
    cursor.execute("""
        SELECT Trainingsplan.*
        FROM Trainingsplan
        JOIN Trainingsplan_Device ON Trainingsplan.ID = Trainingsplan_Device.TrainingsplanID
        WHERE Trainingsplan_Device.DeviceID = ?
    """, (device_id,))
    return cursor.fetchall()



connection.close()