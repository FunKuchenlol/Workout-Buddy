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

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------- INDEX/HOME ---------------------- #
# add_device html template
@app.get("/", name="index")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------- ADD DEVICE ---------------------- #
# add_device html template
@app.get("/add_device")
def add_device(request: Request):
    return templates.TemplateResponse("add_device.html", {"request": request})

# add device magic
@app.post("/add_device")
async def add_new_device(
    name: str = Form(...),
    repetitions: int = Form(...),
    break_time: int = Form(...),
    sets: int = Form(...),
    weight: int = Form(...),
    picture: UploadFile = File(None) 
):
    picture_path_for_db = None

    if picture and picture.filename:
        file_ext = picture.filename.split('.')[-1]
        filename = f"{uuid4()}.{file_ext}"
        full_file_path = os.path.join(UPLOAD_DIR, filename)

        with open(full_file_path, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)

        picture_path_for_db = f"/static/pictures/saved_pictures/{filename}"

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Device (name, repetitions, break_time, sets, weight, picture_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, repetitions, break_time, sets, weight, picture_path_for_db)) 

    conn.commit()
    conn.close()

    return RedirectResponse(url="/", status_code=303)


# ---------------------- DELETE DEVICE ---------------------- #
# delete_device html template
@app.get('/delete_device')
def delete_device(request: Request):
    device_list = read_all_devices()
    return templates.TemplateResponse(
		'delete_device.html', {'request': request, 'devices': device_list}
	)

# delete device magic
@app.post("/delete_device/{device_id}")
async def delete_device_by_id(device_id: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT picture_path FROM Device WHERE id = ?", (device_id,))
    result = cursor.fetchone()

    if result and result[0]:
        picture_path = result[0]
        full_path = picture_path.lstrip('/')
        if os.path.exists(full_path):
            os.remove(full_path)

    cursor.execute("DELETE FROM Device WHERE id = ?", (device_id,))
    conn.commit()
    conn.close()

    return RedirectResponse(url="/delete_device", status_code=status.HTTP_303_SEE_OTHER)

# Confirm delete
@app.post("/delete_device/{device_id}")
async def confirm_delete_device(device_id: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Device WHERE id = ?", (device_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/delete_device", status_code=303)


# ---------------------- EDIT DEVICE ---------------------- #
# edit_device html template
@app.get('/edit_device', response_class=HTMLResponse)
def edit_device(request: Request):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Device")
    devices = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse(
        'edit_device.html', {'request': request, 'devices': devices}
    )

# Get edit_form page
@app.get("/edit_device/{device_id}", response_class=HTMLResponse)
def show_edit_device_form(request: Request, device_id: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Device WHERE id = ?", (device_id,))
    device = cursor.fetchone()
    conn.close()

    return templates.TemplateResponse("edit_form.html", {
        "request": request,
        "device": device
    })

# handle form submission
@app.post("/edit_device/{device_id}")
@app.post("/edit_device/{device_id}")
async def update_device_form(
    device_id: int,
    name: str = Form(...),
    repetitions: int = Form(...),
    break_time: int = Form(...),
    sets: int = Form(...),
    weight: int = Form(...),
    picture: UploadFile = File(None)
):
    picture_path_for_db = None 

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT picture_path FROM Device WHERE id = ?", (device_id,))
    current_picture_path = cursor.fetchone()[0] 

    if picture and picture.filename != "":
        file_ext = picture.filename.split('.')[-1]
        filename = f"{uuid4()}.{file_ext}" 
        full_file_path = os.path.join(UPLOAD_DIR, filename)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        with open(full_file_path, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)

        picture_path_for_db = f"/static/pictures/saved_pictures/{filename}"
        if current_picture_path and current_picture_path.startswith('/static/pictures/saved_pictures/'):
            old_filename = os.path.basename(current_picture_path)
            old_full_file_path = os.path.join(UPLOAD_DIR, old_filename)
            if os.path.exists(old_full_file_path):
                os.remove(old_full_file_path)
                print(f"Altes Bild gelöscht: {old_full_file_path}")

    else:
        picture_path_for_db = current_picture_path

    cursor.execute("""
        UPDATE Device SET name = ?, repetitions = ?, break_time = ?, sets = ?, weight = ?, picture_path = ?
        WHERE id = ?
    """, (name, repetitions, break_time, sets, weight, picture_path_for_db, device_id))

    conn.commit()
    conn.close()
    return RedirectResponse(url="/edit_device", status_code=303)


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

