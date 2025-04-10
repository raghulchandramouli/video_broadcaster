import cv2
import pyvirtualcam

class Streaming():
    
    def __init__(self, in_source=None, out_source=None, fps=None, blur_strength=None, background="none"):
        self.input_source = in_source
        self.out_source = out_source
        self.fps = fps
        self.blur_strength = blur_strength
        self.background = background
        self.running = False
        
    
    def update_streaming_config(self, in_source=None, out_source=None, fps=None, blur_strength=None, background="none"):
        self.input_source = in_source
        self.out_source = out_source
        self.fps = fps
        self.blur_strength = blur_strength
        self.background = background
    
    def stream_video(self):
        self.running = True
        cap = cv2.VideoCapture(int(self.input_source))
        
        frmae_idx = 0
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        
        try:
            self.original_fps = int(cap.get(cv2.CAP_PROP_FSP))
        except Exception as e:
            print(f"Webcam({self.input_source}) live fps not availalbe, set the fps accoringly. Expection : {e}")
            
        if self.fps:
            if self.fps > self.original_fps:
                self.fps = self.original_fps
                frame_interval = int(self.original_fps / self.fps)
            
            else:
                frame_interval = int(self.original_fps / self.fps)
        
        else:
            frame_interval = 1
            
        with pyvirtualcam.Camera(width=width, height=height, fps=self.fps) as cam:
            print(f"Virtual Camara running at {width}x{height} at {self.fps} fps.")
            
            while self.running and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % frame_interval == 0:
                    result = 0 # Model Inference by cv model
                    mask  = 0 # Segmentation mask
                    
                    ### Process masks and create results:
                    result_frame = 0
                    
                    
            cam.send(cv2.cv2Color(result_frame, cv2.COLOR_BGR2RGB))
            cam.sleep_until_next_frame()
            
        cap.release()
    
    def list_available_devices(self):
        devices = []
        
        for i in range(5):        
            cap = cv2.VideoCapture(i)

            if cap.isOpened():
                devices.append({"id": i, "name": f"Camera {i}"})
        return devices