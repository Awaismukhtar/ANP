from concurrent.futures import process
from ntpath import join
import cv2
import numpy as np
import imutils
import easyocr
from time import sleep
import time
import pytesseract

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


class Algorithem:

    def AllowedFile(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def Detect(self, filename):
        # img = cv222.imread('image4.jpg')
        img = cv2.imread(r'static/uploads/' + filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
        edged = cv2.Canny(bfilter, 30, 200)  # Edge detection
        keypoints = cv2.findContours(
            edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = np.array([])

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break

        mask = np.zeros(gray.shape, np.uint8)
        if location.any():
            cv2.drawContours(mask, [location], 0, 255, -1)
            cv2.bitwise_and(img, img, mask=mask)
            # Now crop
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            cropped_image = gray[topx:bottomx+1, topy:bottomy+1]
            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image)
            # pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
            # plate = pytesseract.image_to_string(cropped_image, lang='eng')
            # print("Number plate is:", plate)
            # plate = plate if len(plate) > 4 else ''
            textArray = []
            # if plate == '':
            for (bbox, text, prob) in result:
                print("Vehicel Number", text)
                textArray.append(text)
                plate = "".join(textArray)
                return plate

        return None

    def getCamera(self):
        webcam = cv2.VideoCapture(0)
        processing = True
        image = None
        while processing:
            try:
                timer = time.time()
                if not webcam.isOpened():
                    print('Unable to load camera.')
                    sleep(5)
                    pass
                result, frame = webcam.read()
                # print(result)  # prints true as long as the webcam is running
                if result:
                    # webcam.release()
                    image = frame
                    print("Processing image...")
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
                else:
                    print('no image detected')
                # processing = True
            except (KeyboardInterrupt):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                break
        sleep(10)
        cv2.imwrite(filename='saved_img_{}.jpg'.format(timer), img=image)
        print("Image saved!")

    def gen_frames(self):
        # generate frame by frame from camera
        camera = cv2.VideoCapture(0)
        while True:
            # Capture frame-by-frame
            success, frame = camera.read()  # read the camera frame
            result = frame
            if not success:
                print('assa')
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
                # key = cv2.waitKey(10000)
                # if key == ord('s'):
                #     # saving image in local storage
                #     cv2.imwrite(filename='saved_img.jpg', img=result)
                #     camera.release()
                #     print("here")
                # elif key == ord('q'):
                #     camera.release()
                #     print("q")

                # break
