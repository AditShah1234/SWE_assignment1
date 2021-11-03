from fastapi.encoders import jsonable_encoder
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import math
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
global X,Y ,change
change = False

X=0
Y=0

@app.get('/', response_class=HTMLResponse)
def signin(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/', response_class=HTMLResponse)
async def signin(request: Request, uname: str = Form(...), psw: str = Form(...)):
    print(f'username: {uname}') 
    print(f'password: {psw}')
    name = str(uname)
    password = str(psw)
    get_name = name.lower()
    print(get_name)
    if get_name == "adit" or password=="123":
        
        return RedirectResponse(app.url_path_for('check_cord',**{"Name": name}))
    else:
        return templates.TemplateResponse("login.html", {"request": request})




@app.get('/check_cord/{Name}/', response_class=HTMLResponse)
def check_cord(request: Request, Name: str):
    
    return templates.TemplateResponse("Co-ordinates.html", {"request": request, "Name": Name})

@app.post('/check_cord/{Name}/', response_class=HTMLResponse)
async def check_cord(request: Request,  Name : str):
    global X
    global Y
  
    html = str('https://maps.google.com/maps?q='+str(X)+","+str(Y))
    return templates.TemplateResponse("Co-ordinates.html", {"request": request, "Name": Name, "X" : X, "Y" : Y,"HTML": html})



@app.get("/co-ordinates-input")
def input(request: Request, Name: str, Latitude: float, Longitude: float):
    global X , Y ,change
    
    if math.sqrt((X-Latitude)**2 + (Y-Longitude)**2)> 10:
        change=True

     
    print(change)
    json_compatible_item_data = jsonable_encoder({"X":X, "Y":Y,"X_prev":Latitude, "Y_prev": Longitude, "Aleart": change})
    Y = Longitude
    X = Latitude
    change =False
    return JSONResponse(content=json_compatible_item_data)





if __name__ == "__main__":
    uvicorn.run("app:app",debug=True, port = 8000)