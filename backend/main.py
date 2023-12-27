import shutil
from fastapi import FastAPI, WebSocket, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from chatbot import ChatBotAssistant

UPLOAD_DIR = Path(__file__).resolve().parent / 'uploads'
app = FastAPI()
save_to = ""
# instantiate empty object from chatbot class
def delete_loaded_file(folder_path):
    for file_path in UPLOAD_DIR.glob('*'):
        try:
            if file_path.is_file():
                file_path.unlink()
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

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
    
    global chat_bot_assistant
    data = await file_upload.read()
    save_to = UPLOAD_DIR / file_upload.filename
    delete_loaded_file(str(save_to))

    with open(save_to, 'wb') as f:
        f.write(data)

    chat_bot_assistant = ChatBotAssistant(str(save_to), 
                                        model_name="gpt-3.5-turbo-1106", 
                                        embedding_model_name="text-embedding-ada-002",
                                        summary_length=summary_length, 
                                        details_level=details_level)
    chat_bot_assistant.uploaded_file = str(save_to)
    summary_and_ner = await generate_summary()
    print(summary_and_ner)
    return await generate_summary()




@app.post("/summary/")
async def generate_summary():
    try:
        summary_result = chat_bot_assistant.summarization()
        ner_result = chat_bot_assistant.named_entity_recognition()
        return {
            "summary result": summary_result,
            "ner result": ner_result,    
            }
    except Exception as err:
        return {"summary error": str(err)}

@app.websocket("/ner")
async def generate_ner():
    try:
        ner_result = chat_bot_assistant.named_entity_recognition()

        return {"named entity recognition result": ner_result}
    except Exception as err:
        return {"named entity recognition error": str(err)}

@app.websocket("/ws")
async def chat_bot(websocket: WebSocket):
    print("connecting")
    await websocket.accept
    print("accepted")
    while True:
        try:
            data = await websocket.receive_text
            print(data)
            response = await chat_bot_assistant.send(data)
            await websocket.send_text(response)
        except Exception as err:
            return {"chatbot error": str(err)}

