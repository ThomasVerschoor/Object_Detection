import onnxruntime_gpu-1.4.0-cp36-cp36m-linux_aarch64.whl as onnxruntime


class ModelLoader:
    def __init__(self, onnxfile):
        # path of all the models need to be put right here
        # tinyYolo_object_detection_model = "models/mrcnn.onnx"
        tinyYolo_object_detection_model_light = onnxfile
        # this part of the code will load all types of models right at the beginning, these models will include onnx
        # models made for classification, object detection, etc
        # self.heavy_object_detection_session = onnxruntime.InferenceSession(tinyYolo_object_detection_model, None)
        self.lighter_object_detection_session = onnxruntime.InferenceSession(tinyYolo_object_detection_model_light, None)

    def load_session(self, task):
        if task == 0:
            pass
            #return self.heavy_object_detection_session
        elif task == 1:
            return self.lighter_object_detection_session
        else:
            return None
