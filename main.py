import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import threading

from stream_utils import Streaming

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

stream_thread = None

streaming = Streaming()

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/start")
def start_stream(
    source : str = Query("0"),
    fps : int = Query(15),
    blur : int = Query(21),
    background : str = Query("none")
):
    global stream_thread
    
    # Check if stream is already running and stop it first
    if streaming.running:
        streaming.update_running_status(False)
        if stream_thread and stream_thread.is_alive():
            stream_thread.join(timeout=1.0)  # Wait for thread to finish
    
    # Update configuration with new parameters
    streaming.update_streaming_config(
        in_source=source,
        out_source=None, 
        fps=fps,
        blur_strength=blur,
        background=background
    )
    
    # Start new streaming thread
    stream_thread = threading.Thread(
        target=streaming.stream_video,
        args=()
    )
    
    stream_thread.start()
    
    return {"message" : f"Streaming started from source: {source} with {fps} FPS and blur strength: {blur}."}

@app.get("/stop")
def stop_stream():
    return streaming.update_running_status()

@app.get("/devices")
def devices():
    return streaming.list_available_devices()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)