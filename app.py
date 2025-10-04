from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.components.predictor import Predictor
from src.logger import logging
from src.exception import CustomException
import sys


logger=logging.getLogger('app')


app = FastAPI(title="Student Performance Prediction API")
templates = Jinja2Templates(directory="templates")

# Initialize pipeline once
predictor =Predictor()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    gender: str = Form(...),
    race_ethnicity: str = Form(...),
    parental_level_of_education: str = Form(...),
    lunch: str = Form(...),
    test_preparation_course: str = Form(...),
    reading_score: int = Form(...),
    writing_score: int = Form(...)
):
    try:
        input_data = {
            "gender": gender,
            "race/ethnicity": race_ethnicity,
            "parental level of education": parental_level_of_education,
            "lunch": lunch,
            "test preparation course": test_preparation_course,
            "reading score": reading_score,
            "writing score": writing_score
        }

        # Predict
        prediction = predictor.predict(input_data)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "prediction": prediction
            }
        )
    except Exception as e:
        logger.error(e)
        raise CustomException(e,sys)

