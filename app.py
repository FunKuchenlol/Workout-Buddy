import sqlite3
import os
import shutil
from uuid import uuid4

from fastapi import FastAPI, Form, Request, UploadFile, File, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cruds.device import read_all_devices, create_device

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

UPLOAD_DIR = "static/pictures/saved_pictures"
DB = "WorkoutBuddy.sqlite"

# Stellen Sie sicher, dass das Upload-Verzeichnis existiert
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------- INDEX/HOME: FORM ---------------------- #
@app.get("/", name="index")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------- ADD DEVICE: FORM ---------------------- #
@app.get("/add_device")
def add_device(request: Request):
    return templates.TemplateResponse("add_device.html", {"request": request})
# ---------------------- ADD DEVICE: CREATE DEVICE (with picture) ---------------------- #
@app.post("/add_device")
async def add_new_device(
    name: str = Form(...),
    repetitions: int = Form(...),
    break_time: int = Form(...),
    sets: int = Form(...),
    weight: int = Form(...),
    picture: UploadFile = File(None) 
):
    # Standardpfad für den Fall, dass kein Bild hochgeladen wird
    picture_path_for_db = None

    if picture and picture.filename:
        # Ein Bild wurde hochgeladen, speichere es
        file_ext = picture.filename.split('.')[-1]
        filename = f"{uuid4()}.{file_ext}"
        full_file_path = os.path.join(UPLOAD_DIR, filename)

        with open(full_file_path, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)

        # Der Pfad, der in der Datenbank gespeichert wird (relativ zum static-Verzeichnis)
        picture_path_for_db = f"/static/pictures/saved_pictures/{filename}"

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Device (name, repetitions, break_time, sets, weight, picture_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, repetitions, break_time, sets, weight, picture_path_for_db)) # <--- Hier den generierten Pfad verwenden

    conn.commit()
    conn.close()

    return RedirectResponse(url="/", status_code=303)


# ---------------------- DELETE DEVICE: FORM ---------------------- #
@app.get('/delete_device')
def delete_device(request: Request):
    device_list = read_all_devices()
    return templates.TemplateResponse(
		'delete_device.html', {'request': request, 'devices': device_list}
	)
# ---------------------- DELETE DEVICE: DELETE DEVICE (with picture) ---------------------- #
@app.post("/delete_device/{device_id}")
def delete_device_by_id(device_id: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Bildpfad herausfinden
    cursor.execute("SELECT picture_path FROM Device WHERE id = ?", (device_id,))
    result = cursor.fetchone()

    if result and result[0]:
        picture_path = result[0]
        full_path = picture_path.lstrip('/')
        if os.path.exists(full_path):
            os.remove(full_path)

    # Gerät löschen
    cursor.execute("DELETE FROM Device WHERE id = ?", (device_id,))
    conn.commit()
    conn.close()

    return RedirectResponse(url="/delete_device", status_code=status.HTTP_303_SEE_OTHER)

# ---------------------- DELETE DEVICE: FORM ---------------------- #
@app.post("/delete_device/{device_id}")
def confirm_delete_device(device_id: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Device WHERE id = ?", (device_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/delete_device", status_code=303)


# ---------------------- EDIT DEVICE ---------------------- #
@app.get('/edit_device')
def edit_device(request: Request):
    return templates.TemplateResponse(
		'edit_device.html', {'request': request}
	)


# ---------------------- ALL DEVICES ---------------------- #
@app.get('/all_devices')
def all_devices(request: Request):
    device_list = read_all_devices()
    return templates.TemplateResponse(
		'all_devices.html', {'request': request, 'devices': device_list}
	)


# ---------------------- ABOUT ---------------------- #
@app.get('/about')
def about(request: Request):
    return templates.TemplateResponse(
		'about.html', {'request': request}
	)

