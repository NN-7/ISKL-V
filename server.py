import uvicorn
import os
from fastapi import FastAPI, Request, UploadFile, File

app = FastAPI()


@app.post("/")
async def get_file(request: Request, file: UploadFile = File(...)):
    IP = request.client.host
    os.makedirs(IP, exist_ok=True)
    contents = await file.read()
    with open(f"{IP}/{file.filename}", 'wb') as f:
        f.write(contents)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)