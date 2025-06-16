from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cruds.device import read_all_devices, create_device

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

# ---------------------- INDEX/HOME ---------------------- #

@app.get('/', name='index')
def index(request: Request):
    return templates.TemplateResponse(
		'index.html', {'request': request}
	)


# ---------------------- ADD DEVICE ---------------------- #

@app.get('/add_device')
def add_device(request: Request):
    return templates.TemplateResponse(
		'add_device.html', {'request': request}
	)

@app.post('/add_device')
def add_new_device(
    name: str = Form(...),
    active_time: int = Form(...),
    break_time: int = Form(...),
    sets: int = Form(...),
    picture_path: str = Form(...)
):
    create_device(name, active_time, break_time, sets, picture_path)
    return RedirectResponse(url="/", status_code=303)


# ---------------------- DELETE DEVICE ---------------------- #
@app.get('/delete_device')
def delete_device(request: Request):
    return templates.TemplateResponse(
		'delete_device.html', {'request': request}
	)


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

