import cv2
import mediapipe as md
import csv
import datetime

md_drawing = md.solutions.drawing_utils
md_pose = md.solutions.pose

count = 0
prev_count = 0
position = None
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

total_count = 0
pushup_start_time = None
pushup_end_time = None

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
filename = f"{current_date}.csv"

with md_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose, open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Total Push-up Count", "Start Time", "End Time"])

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Empty camera")
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, "", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = image[y:y + h, x:x + w]

        result = pose.process(image)
        imlist = []

        if result.pose_landmarks:
            md_drawing.draw_landmarks(image, result.pose_landmarks, md_pose.POSE_CONNECTIONS)
            for id, im in enumerate(result.pose_landmarks.landmark):
                h, w, _ = image.shape
                X, Y = int(im.x * w), int(im.y * h)
                imlist.append([id, X, Y])

        if len(imlist) != 0:
            if ((imlist[12][2] - imlist[14][2]) >= 15 and (imlist[11][2] - imlist[13][2]) >= 15):
                if position != "down":
                    position = "down"
                    if pushup_start_time is None:
                        pushup_start_time = datetime.datetime.now()
            if ((imlist[12][2] - imlist[14][2]) <= 5 and (imlist[11][2] - imlist[13][2]) <= 5) and position == "down":
                if position != "up":
                    position = "up"
                    count += 1
                    pushup_end_time = datetime.datetime.now()
                    if count != prev_count:
                        prev_count = count
                        cv2.rectangle(image, (50, 10), (200, 60), (0, 0, 0), -1)
                        cv2.putText(image, f'Count: {count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        print(f'Count: {count}')


        if count > total_count:
            total_count = count

        cv2.imshow("Push-up counter", image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            pushup_end_time = datetime.datetime.now()
            break

    writer.writerow(["Sahil", total_count, pushup_start_time.strftime("%H:%M:%S"), pushup_end_time.strftime("%H:%M:%S")])

cap.release()
cv2.destroyAllWindows()                                      
                                      