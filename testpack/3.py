txt='''researchers in practical scenes, and we also provide de-
ploy versions with ONNX, TensorRT, NCNN, and Openvino
supported. Source code is at https://github.com/
Megvii-BaseDetection/YOLOX .
1. Introduction
With the development of object detection, YOLO se-
ries [23, 24, 25, 1, 7] always pursuit the optimal speed and
accuracy trade-off for real-time applications. They extract
the most advanced detection technologies available at the
time (e.g., anchors [26] for YOLOv2 [24], Residual Net [9]
for YOLOv3 [25]) and optimize the implementation for best
practice. Currently, YOLOv5 [7] holds the best trade-off
performance with 48.2% AP on COCO at 13.7 ms.1
Nevertheless, over the past two years, the major ad-
vances in object detection academia have focused on
anchor-free detectors [29, 40, 14], advanced label assign-'''
lines = txt.split('\n')
for line in lines:
    print(line)