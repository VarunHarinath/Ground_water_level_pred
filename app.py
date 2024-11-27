from fastapi import FastAPI,Depends,HTTPException,Header
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import numpy as np
import pandas as pd
import pickle
from datetime import date
from mongo_model import GroundWaterModel,MongoDB

app = FastAPI()

API_KEYS = {
    "AJUOBVYUI9U1JD8",
    "KNDP3938FGRGEFV",
    "CN2957BNH934TYOJ"
}

class request_response_model(BaseModel):
    Temperature_C: float
    Rainfall_mm: float
    Dissolved_Oxygen_mg_L: float
    
class response_model(BaseModel):
    rain_fall_predtiction: float
    predicted_date: str = date.today().strftime('%d-%m-%Y')
    prdiction:bool=True


with open('ground_water_level.pkl','rb') as f:
    model = pickle.load(f)


def verify_api_keys(x_api_key:str=Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=404,detail="Invalid API Key")
    return x_api_key

@app.post('/make_prediction')
async def home(request:request_response_model,x_api_key:str=Depends(verify_api_keys)):
    df = pd.DataFrame([request.dict().values()],columns=request.dict().keys())
    prediction = model.predict(df)
    response = response_model(rain_fall_predtiction=prediction[0])
    return JSONResponse(content=response.dict(),status_code=200,headers={"x-api-key":x_api_key})


