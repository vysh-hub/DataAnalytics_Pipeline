from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

from pipeline import clean_data, generate_insights

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

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)

    df = clean_data(df)

    insights = generate_insights(df)

    return insights