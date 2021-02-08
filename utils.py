# from google.colab import drive
# drive.mount('/content/gdrive')

# cd 'gdrive/My Drive/Colab Notebooks'

"""**1. Importing Modules**"""

# 1. IMPORTING MODULES
import cv2
import numpy as np
from tensorflow.keras.models import load_model

"""**2. Loading the Pre-trained OCR CNN Model**"""

# 2. LOADING THE PRE-TRAINED OCR CNN MODEL
def initialize_prediction_model():
    model = load_model('digit_model.h5')
    return model

"""**3. Pre-processing the Image**"""

# 3. PRE-PROCESSING THE IMAGE
def pre_process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE. REQUIRED INPUT FORMAT FOR BLUR AND THRESHOLD
    # ADD GAUSSIAN BLUR TO SMOOTHEN THE IMAGE AND REMOVE HIGH FREQUENCY NOISE (Low-Pass Filter)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    # APPLY ADAPTIVE THRESHOLD TO OBTAIN INVERTED BINARY IMAGE WITH BLACK BACKGROUND AND WHITE CHARACTERS
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, 1, 1, 11, 2)
    return img_threshold

"""**5.1 Find the Biggest Contour assuming that it's the Sudoku Board**"""

# 5.1 FIND THE BIGGEST CONTOUR ASSUMING THAT IT'S THE SUDOKU BOARD
def get_biggest_contour(contours):
    biggest = np.array([])
    max_area = 0

    for i in contours:
        area = cv2.contourArea(i)

        # IGNORING VERY SMALL (/INSIGNIFICANTLY SIZED) CONTOURS
        if area > 50:
            perimeter = cv2.arcLength(i, True)  # CALCULATE PERIMETER FOR CLOSED CONTOUR
            # APPROXIMATE THE NUMBER OF VERTICES IN A CLOSED CONTOUR USING 'Douglas-Peucker' ALGORITHM
            approx_vertices = cv2.approxPolyDP(i, 0.02 * perimeter, True)

            # IDENITFY THE CONTOUR WITH THE LARGEST AREA AND FOUR BOUNDARY VERTICES i.e. SUDOKU BOARD
            if area > max_area and len(approx_vertices) == 4:
                biggest = approx_vertices
                max_area = area

    return biggest, max_area

def reorder(board_vertices):
    board_vertices = board_vertices.reshape((4, 2))
    print(board_vertices)
    board_vertices_copy = np.zeros((4, 1, 2), dtype=np.int32)
    print(board_vertices_copy)
    add = np.sum(board_vertices, axis=1)
    # board_vertices.sum(1)
    print(add)
    board_vertices_copy[0] = board_vertices[np.argmin(add)]
    board_vertices_copy[3] = board_vertices[np.argmax(add)]
    diff = np.diff(board_vertices, axis=1)
    print(diff)
    board_vertices_copy[1] = board_vertices[np.argmin(diff)]
    board_vertices_copy[2] = board_vertices[np.argmax(diff)]
    return board_vertices_copy

def split_boxes(img):
    rows = np.vsplit(img,9)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,9)
        for box in cols:
            boxes.append(box)
    return boxes

def get_prediction(boxes,model):
    result = []
    for image in boxes:
        # PREPARE IMAGE
        img = np.asarray(image)
        img = img[4:img.shape[0]-4, 4:img.shape[1]-4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        # GET PREDICTION
        predictions = model.predict(img)
        class_index = model.predict_classes(img)
        probability_value = np.amax(predictions)
        # SAVE TO RESULT
        if probability_value > 0.8:
            result.append(class_index[0])
        else:
            result.append(0)
    return result

# 5 TO DISPLAY THE SOLUTION ON THE IMAGE
def display_numbers(img,numbers,color = (0,255,0)):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for x in range (0,9):
        for y in range (0,9):
            if numbers[(y*9)+x] != 0 :
                 cv2.putText(img, str(numbers[(y*9)+x]),
                               (x*secW+int(secW/2)-10, int((y+0.8)*secH)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            2, color, 2, cv2.LINE_AA)
    return img

def draw_grid(img):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)
    return img

# import tensorflow as tf
# print(cv2.__version__)
# print(tf.__version__)
# import keras
# print(keras.__version__)
# import sys
# print(sys.version_info)