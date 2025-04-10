import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from stream_utils import Streaming

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


streaming = Streaming()

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/start")
def start_stream(
    source : str = Query("0"),
    fps : int = Query(15),
    blur_strength : int = Query(21),
    background : str = Query("none")
):
    
    streaming.update_streaming_config(in_source=None, out_source=None, fps=None, blur_strength=None, background="none")
    return 0

@app.get("/devices")
def devices():
    return streaming.list_available_devices()

def a(a, b, c, d):
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)