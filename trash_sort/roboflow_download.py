
from roboflow import Roboflow
rf = Roboflow(api_key="hhGdvI8f5C6he2aJHkwZ")
project = rf.workspace("school-kxuuy").project("deneme-nvvno")
version = project.version(3)
dataset = version.download("yolov8")
                