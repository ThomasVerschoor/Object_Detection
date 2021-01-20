import onnxruntime


class ModelLoader:
    def __init__(self, onnxmodel):
        # path of all the models need to be put right here
        # tinyYolo_object_detection_model = "models/mrcnn.onnx"
        # this part of the code will load all types of models right at the beginning, these models will include onnx
        # models made for classification, object detection, etc
        # self.heavy_object_detection_session = onnxruntime.InferenceSession(tinyYolo_object_detection_model, None)
        self.lighter_object_detection_session = onnxruntime.InferenceSession(onnxmodel, None)
        print(onnxruntime.get_device())

    def load_session(self, task):
        if task == 0:
            pass
            #return self.heavy_object_detection_session
        elif task == 1:
            return self.lighter_object_detection_session
        else:
            return None
