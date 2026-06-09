from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app=FastAPI()

model = joblib.load("models/model.pkl")
encoder = joblib.load("models/encoder.pkl")
airline_delay_rate = joblib.load("models/airline_delay_rate.pkl")
origin_delay_rate = joblib.load("models/origin_delay_rate.pkl")
route_delay_predictor = joblib.load("models/route_delay_rate.pkl")


class flight(BaseModel):
    month: int
    day_of_month: int
    day_of_week: int
    airline: str
    origin: str
    dest: str
    dep_hour: int
    crs_elapsed_time: float
    distance: float


@app.post("/predict")
def predict(features:flight):
    data=pd.DataFrame([features.model_dump()])
    data = data.rename(columns={"airline": "op_unique_carrier"})
    for col in ["op_unique_carrier", "origin", "dest"]:
        data[col] = encoder[col].transform(data[col])
    data["is_rush_hour"] = int(features.dep_hour in [7,8,9,17,18,19])
    data["is_holiday_month"] = int(features.month in [7,8,12,1])
    data["is_weekend"] = int(features.day_of_week in [5,6,7])
    data["is_short_flight"] = int(features.distance < 500)
    data["airline_delay_rate"] = airline_delay_rate.get(data["op_unique_carrier"][0], 0.2)
    data["origin_delay_rate"] = origin_delay_rate.get(data["origin"][0], 0.2)
    data["route_delay_rate"] = route_delay_predictor.get((data["origin"][0], data["dest"][0]), 0.2)

    feature_order = model.feature_name_
    data = data[feature_order]
    prediction = model.predict(data)[0]
    prediction=model.predict(data)[0]
    result= "Delayed " if prediction==1 else "On time"
    return {"prediction":result}

