FROM mcr.microsoft.com/azureml/onnxruntime:v.1.4.0-jetpack4.4-l4t-base-r32.4.3

# make a dir for application
WORKDIR /app  
# install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip libprotobuf-dev protobuf-compiler python-scipy
RUN apt-get install -y wget
RUN pip3 install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN wget https://github.com/onnx/models/blob/master/vision/object_detection_segmentation/faster-rcnn/model/FasterRCNN-10.onnx?raw=true
RUN wget https://raw.githubusercontent.com/onnx/models/master/vision/object_detection_segmentation/faster-rcnn/dependencies/coco_classes.txt
#RUN wget https://github.com/onnx/models/blob/master/vision/object_detection_segmentation/faster-rcnn/dependencies/demo.jpg?raw=true
# copy source code
COPY  /app .
#run application
CMD [ "python3", "cam_object_detection.py", "FasterRCNN-10.onnx?raw=true"]