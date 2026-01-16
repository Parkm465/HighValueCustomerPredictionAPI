from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from sklearn.linear_model import LinearRegression
from pydantic import BaseModel
import joblib
import pandas as pd


app = FastAPI()
THRESHOLD = 0.6


@app.get('/')
def root():
  return {'message' : 'API is working'}

class Features(BaseModel):
  # Recency, Frequency, Monetary, spend_last_90_days, SpendTrend, AverageOrderValue
  Recency: float
  Frequency: float
  Monetary: float
  spend_last_90_days: float
  SpendTrend: float
  AverageOrderValue: float

pipe = joblib.load('mymodel.joblib')

# Define prediction endpoint
@app.post('/predict')
def predict(data: Features):
  test_data = pd.DataFrame([data.dict()])
  prob = pipe.predict_proba(test_data)[0][1]
  pred = 'High Value' if prob >=THRESHOLD else "Not High Value"
  return {'high_value_probability' : prob, 
          'prediction' :pred,
          'status' : 'success'}

@app.get('/health')
def health():
  return {'status' : 'ok'}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
  message = 'Validation Error'
  for error in exc.errors():
    message += f"\nField: {error['loc']}, Error: {error['msg']}"
  return PlainTextResponse(message, status_code=400)