from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cruds.device import read_all_devices, create_device

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/')
def index(request: Request):
    device_list = read_all_devices()
    return templates.TemplateResponse(
		'index.html', {'request': request, 'devices': device_list}
	)

@app.get('/add-device')
def add_device(request: Request):
    return templates.TemplateResponse(
		'add_device.html', {'request': request}
	)

@app.post('/add-device')
def add_new_device(
    name: str = Form(...),
    active_time: int = Form(...),
    break_time: int = Form(...),
    sets: int = Form(...),
    picture_path: str = Form(...)
):
    create_device(name, active_time, break_time, sets, picture_path)
    return RedirectResponse(url="/", status_code=303)


    