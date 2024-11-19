from ultralytics import YOLO

model = YOLO("yolov8m.pt")

results = model.predict("https://www.oiseaux.net/photos/robert.balestra/images/rougegorge.familier.roba.1g.jpg")

result = results[0]
box = result.boxes
#print("Object type:", box.cls)
#print("Coordinates:", box.xyxy)
#print("Probability:", box.conf)

cords = box.xyxy[0].tolist()
class_id = result.names[box.cls[0].item()]
conf = box.conf[0].item()
print("Object type:", class_id)
print("Coordinates:", cords)
print("Probability:", conf)