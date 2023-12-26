from fastapi import FastAPI, WebSocket, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

UPLOAD_DIR = Path() / 'uploads'
app = FastAPI()

# instantiate empty object from chatbot class
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/")
async def create_upload_file(file_upload: UploadFile, 
                             summary_length: int = 3,
                             details_level: str = "abstract"):
    data = await file_upload.read()
    save_to = UPLOAD_DIR / file_upload.filename
    with open(save_to, 'wb') as f:
        f.write(data)

    # instantiate object + path and send it to chatbot 
    return {"filename uploaded successfully": file_upload.filename} 

@app.websocket("/summary")
async def generate_summary():
    # instantiate object from 
    pass

@app.websocket("/ner")
async def generate_ner():
    pass

@app.websocket("/ws")
async def chat_bot(websocket: WebSocket):
    pass
