from fastapi import FastAPI, Query, HTTPException, Depends
from typing import List
from io import BytesIO
from pathlib import Path

app = FastAPI(version='0.1', title='Wiki Audio Maker')

@app.get("/api")
async def root():
    return {"Wiki": "trivago"}