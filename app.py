import sqlite3
import os
import shutil
from uuid import uuid4

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cruds.device import read_all_devices, create_device, update_device, delete_device 

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

UPLOAD_DIR = "static/pictures/saved_pictures"
DB = "WorkoutBuddy.sqlite" 
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------- INDEX PAGE ---------------------- #
@app.get("/", name="index")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------------- DEVICES PAGE ---------------------- #
@app.get("/devices", name="devices") 
async def get_devices_page(request: Request):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, repetitions, break_time, sets, weight, picture_path FROM Device")
    devices = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse("devices.html", {"request": request, "devices": devices})


# ---------------------- CREATE DEVICE (POST) ---------------------- #
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
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(full_file_path, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
        picture_path_for_db = f"/static/pictures/saved_pictures/{filename}"

    create_device(name, repetitions, break_time, sets, weight, picture_path_for_db)
    
    return RedirectResponse(url="/devices", status_code=303)


# ---------------------- UPDATE DEVICE (POST) ---------------------- #
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
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT picture_path FROM Device WHERE id = ?", (device_id,))
    result = cursor.fetchone()
    current_picture_path_db = result[0] if result else None
    picture_path_to_save = current_picture_path_db

    if picture and picture.filename != "":
        if current_picture_path_db and current_picture_path_db.startswith('/static/pictures/saved_pictures/'):
            old_filename = os.path.basename(current_picture_path_db)
            old_full_file_path = os.path.join(UPLOAD_DIR, old_filename)
            if os.path.exists(old_full_file_path):
                os.remove(old_full_file_path)
        
        file_ext = picture.filename.split('.')[-1]
        filename = f"{uuid4()}.{file_ext}"
        full_file_path = os.path.join(UPLOAD_DIR, filename)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(full_file_path, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
        picture_path_to_save = f"/static/pictures/saved_pictures/{filename}"

    update_device(device_id, name, repetitions, break_time, sets, weight, picture_path_to_save)
    
    return RedirectResponse(url="/devices", status_code=303)

# ---------------------- DELETE DEVICE (POST) ---------------------- #
@app.post("/delete_device/{device_id}")
async def delete_device_route(device_id: int): 
    conn = sqlite3.connect(DB) 
    cursor = conn.cursor()

    cursor.execute("SELECT picture_path FROM Device WHERE id = ?", (device_id,))
    result = cursor.fetchone()    
    picture_path_to_delete = result[0] if result else None    
    conn.close() 
    delete_device(device_id) 

    if picture_path_to_delete and picture_path_to_delete.startswith('/static/pictures/saved_pictures/'):
        old_filename = os.path.basename(picture_path_to_delete)
        old_full_file_path = os.path.join(UPLOAD_DIR, old_filename)
        if os.path.exists(old_full_file_path):
            os.remove(old_full_file_path)

    return RedirectResponse(url="/devices", status_code=303)

# ---------------------- ABOUT PAGE ---------------------- #
@app.get("/about", name="about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
