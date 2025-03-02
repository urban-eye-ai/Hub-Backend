
import torch

CONF_THRESHOLD = 0.3
IOU_THRESHOLD = 0.5

class DetectionModel:
    def __init__(self, model_name: str):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        model.conf = CONF_THRESHOLD
        model.iou = IOU_THRESHOLD
        self.model = model
    
    def detect(self, frame):
        results = self.model(frame)
        return results

    def names(self):
        return self.model.names