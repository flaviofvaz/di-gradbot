from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uuid
import shutil
import os
from typing import List, Dict


indexed_files = {}
local_filepaths = "./saved_files/"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "api is alive!"}


@app.post("/documents/insert")
async def insert_document(file: UploadFile = File(...)):
    # ensure files can be saved - directory exists
    if not os.path.isdir(local_filepaths):
        os.mkdir(local_filepaths)
    # file already indexed -  need to remove it and re-add it if you want to re-index it
    if file.filename in indexed_files:
        return {"filename": file.filename, "message": "file already indexed."}

    # define the path where you want to save the file
    file_location = f"{local_filepaths}/{file.filename}"
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()
        indexed_files[file.filename] = uuid.uuid4().hex

    # TODO: index file
    return {"filename": file.filename, "message": "file indexed successfully"}


@app.post("/documents/remove")
async def remove_document(filename: str):
    if filename in indexed_files:
        os.remove(f"{local_filepaths}/{filename}")
        # TODO: remove chunks from vector database

        del indexed_files[filename]
        return {"filename": filename, "message": "removed successfully."}
    else:
        return {"filename": filename, "message": "file not found."}


@app.post("/chat/interact")
async def chat_interaction(messages: List[Dict[str, str]]):
    print(messages)
    return {"message": "i'm a mock"}
