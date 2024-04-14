from roboflow import Roboflow
rf = Roboflow(api_key="hhGdvI8f5C6he2aJHkwZ")
project = rf.workspace("julien-vadeboncoeur-xvuem").project("door-handle-segmentation")
version = project.version(19)
dataset = version.download("yolov8")

###문고리 종류별로 segmentation 된거임.
###https://universe.roboflow.com/julien-vadeboncoeur-xvuem/door-handle-segmentation