from fastapi import FastAPI, Request, Form
from typing import Optional
import os
from joblib import load
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.components.model_predictor import CostPredictor, shippingData
from src.constants import APP_HOST, APP_PORT
from src.pipeline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_ID = os.getenv("AdminID")
ADMIN_PASSWORD = os.getenv("AdminPassword")

try:    
    model = load('ShipmentPrice-Prediction/best_model/shipping_price_model.pkl')
except Exception as e:
    model = None
    
print(model)

class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.artist: Optional[str] = None
        self.height: Optional[str] = None
        self.width: Optional[str] = None
        self.weight: Optional[str] = None
        self.material: Optional[str] = None
        self.priceOfSculpture: Optional[str] = None
        self.baseShippingPrice: Optional[str] = None
        self.international: Optional[str] = None
        self.expresssrc: Optional[str] = None
        self.installationIncluded: Optional[str] = None
        self.transport: Optional[str] = None
        self.fragile: Optional[str] = None
        self.customerInformation: Optional[str] = None
        self.remoteLocation: Optional[str] = None

    async def get_shipping_data(self):
        form = await self.request.form()
        self.artist = form.get("artist")
        self.height = form.get("height")
        self.width = form.get("width")
        self.weight = form.get("weight")
        self.material = form.get("material")
        self.priceOfSculpture = form.get("priceOfSculpture")
        self.baseShippingPrice = form.get("baseShippingPrice")
        self.international = form.get("international")
        self.expresssrc = form.get("expresssrc")
        self.installationIncluded = form.get("installationIncluded")
        self.transport = form.get("transport")
        self.fragile = form.get("fragile")
        self.customerInformation = form.get("customerInformation")
        self.remoteLocation = form.get("remoteLocation")

@app.get("/", name="home")
async def home(request: Request):
    return templates.TemplateResponse(
            "home.html",
            {"request": request, "name": model}
        )

@app.post("/admin_login", name="admin_login")
async def admin_login(adminID: str = Form(...), adminPassword: str = Form(...)):
    if adminID == ADMIN_ID and adminPassword == ADMIN_PASSWORD:
        return JSONResponse(content={"success": True})
    return JSONResponse(content={"success": False})

@app.get("/train", name="train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict", name="predict")
async def predictGetRouteClient(request: Request):
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "context": ""},
        )
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/predict", name="predict")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_shipping_data()
        shipping_data = shippingData(
            artist=form.artist,
            height=form.height,
            width=form.width,
            weight=form.weight,
            material=form.material,
            priceOfSculpture=form.priceOfSculpture,
            baseShippingPrice=form.baseShippingPrice,
            international=form.international,
            expresssrc=form.expresssrc,
            installationIncluded=form.installationIncluded,
            transport=form.transport,
            fragile=form.fragile,
            customerInformation=form.customerInformation,
            remoteLocation=form.remoteLocation,
        )
        cost_df = shipping_data.get_input_data_frame()
        cost_predictor = CostPredictor()
        cost_value = round(cost_predictor.predict(X=cost_df)[0], 2)
        cost_message = f"Shipment Price is: {cost_value:.2f}"
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "context": cost_message},
        )
    except Exception as e:
        return {"status": False, "error": f"{e}"}

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)