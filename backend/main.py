from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pipeline import profile_data, clean_data, generate_insights
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "datasets")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_FOLDER = "../data"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.post("/upload")
async def upload_csv(file: UploadFile):

    file_path = os.path.join(UPLOAD_FOLDER, "current.csv")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)

    profile = profile_data(df)

    return profile
@app.post("/clean")
async def run_cleaning(config: dict):

    file_path = os.path.join(UPLOAD_FOLDER, "current.csv")

    df = pd.read_csv(file_path)

    rows_before = len(df)

    df = clean_data(df, config)

    rows_after = len(df)

    df.to_csv(file_path, index=False)

    return {
        "rows_before": rows_before,
        "rows_after": rows_after
    }
@app.get("/insights")
async def get_insights():

    file_path = os.path.join(UPLOAD_FOLDER, "current.csv")

    df = pd.read_csv(file_path)

    insights = generate_insights(df)

    return insights