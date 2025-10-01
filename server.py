import uvicorn
import os
from fastapi import FastAPI, Request

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

@app.post("/")
async def recieve_file(request: Request):
    os.makedirs(request.client.host) # make a folder for files recieved from each IP so it's organized
    body = (await request.body()).decode('utf-8') # get the body text and turn it into a workable string
    file_content = get_file_content(body, request.headers) # get the file content
    filename = get_filename(body) # get the filename
    with open(f"{request.client.host}/{filename}", 'w') as f:
        f.write(file_content)


# Example of an HTTP request to illustrate what the code does
# ----------------------------916537567078260252312735
# Content-Disposition: form-data; name=""; filename="simplefile.png"
# Content-Type: image/png
# 
# FILE CONTENT HERE
# ----------------------------916537567078260252312735--
    
def get_file_content(request_body, request_headers):
    headers_split_index = request_headers['content-type'].find('boundary=') + 9 # get the index of where the boundary descriptor starts
    boundary = '--' + request_headers['content-type'][headers_split_index:] # remove all text which isn't the boundary descriptor
    
    content_type_index = request_body.find('Content-Type') # essentially get the index of the last line before the file content starts
    next_line_index = content_type_index + request_body[content_type_index:].find('\n')+3 # get the \n of the last line before the file content starts and the next unneccasary \n(s) so only the file content will remain
    end_boundary_index = content_type_index + request_body[content_type_index:].find(boundary)-1 # get the index of where the file ends, and remove the \n which ends the file content
    file = request_body[next_line_index:end_boundary_index] # remove everything but the file content

    return file

def get_filename(request_body):
    filename_index = request_body.find('filename="')+10 # get the index of where the file name starts
    filename_end_index = filename_index + request_body[filename_index:].find('"') # get the index of the end of the filename
    filename = request_body[filename_index:filename_end_index] # get the filename
    return filename
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# --------------------------693827015487970523496328
