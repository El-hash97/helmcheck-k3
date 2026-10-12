from ultralytics import YOLO
import cv2

model = YOLO("runs/helmet/weights/best.pt")  # hasil train_colab.ipynb

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.4, verbose=False)
    annotated = results[0].plot()

    cv2.imshow("Helmet Detection - YOLOv8", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
