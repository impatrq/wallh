import sqlite3


conn = sqlite3.connect("Hospital.db", check_same_thread=False)
cursor= conn.cursor()

cmd = '''CREATE TABLE IF NOT EXISTS Pacientes(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMBRE TEXT ,
    APELLIDO TEXT,
    DNI INTEGER ,
    TEMPERATURA FLOAT,
    OXIGENO FLOAT ,
    PULSO INTEGER 
    ) '''
cursor.execute(cmd)

def añadirPaciente(nombre, apellido, dni):
    cmd = f'''INSERT INTO Pacientes (NOMBRE, APELLIDO, DNI, TEMPERATURA, OXIGENO, PULSO) VALUES ("{nombre}", "{apellido}", {dni}, {0}, {0}, {0})'''
    cursor.execute(cmd)
    conn.commit()

def updateMediciones(id, temperatura, oxigeno, pulso):
    cmd = f'''UPDATE Pacientes SET TEMPERATURA={temperatura}, OXIGENO={oxigeno}, PULSO={pulso} WHERE ID={id}'''
    cursor.execute(cmd)
    conn.commit()

def eliminarPaciente(dni):
    cmd = f'''DELETE FROM Pacientes WHERE (DNI="{dni}")'''
    cursor.execute(cmd)
    conn.commit()

def getPacientes():
    cmd = f'''SELECT * FROM Pacientes'''
    cursor.execute(cmd)
    pacientes = cursor.fetchall()
    return pacientes