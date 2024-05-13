import cv2
import pytesseract
from PIL import Image
import re

harcascade = "model/haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)

cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
count = 0


allowed_plates = ["1623924", "23924"]


def FilterVehicles(plate):
    for allowed_number in allowed_plates:
        set1 = set(str(allowed_number))
        set2 = set(str(plate))
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        if (len(intersection) / len(union) >= 0.7) and (len(plate.strip()) == len(allowed_number)):
            print(plate, "allowed", len(intersection) / len(union))


def extractText(image):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(pil_image)
    print("text", text)
    filtered_text = re.sub(r'\D', '', text)  # Remove non-numeric characters
    # Print the extracted text
    print('filtered_text' + filtered_text)
    if filtered_text:
        # Check if the filtered text is similar to an allowed plate and print a message
        if FilterVehicles(filtered_text):
            print("Plate is similar to an allowed plate!")


while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)

    cv2.imshow("Result", img)
    extractText(img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", img_roi)
        cv.rectangle(img, (0, 200), (640, 300),
                     (0, 255, 0), cv2.FILLED)  # Typo fix
        cv2.putText(img, "Plate Saved", (150, 265),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results", img)
        cv2.waitKey(500)
        count += 1
