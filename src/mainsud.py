# 0. Mounting Google Drive


# from google.colab import drive
# drive.mount('/content/gdrive')

# cd 'gdrive/My Drive/Colab Notebooks'

"""**1. Importing Essential Modules**"""

# Commented out IPython magic to ensure Python compatibility.
# 1. IMPORTING ESSENTIAL MODULES
#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# Comment when using python files
# %run utils.ipynb
# %run SudokuSolver.ipynb

##########
# Uncomment when using python files
# import sys
# sys.path.append('C:/Users/Mohak.Manghirmalani/OneDrive - EY/Documents/misc/Sudoku')
from src.utils import *
# from SudokuSolver import SudukoSolver
import src.SudokuSolver as SudokuSolver
##########

"""**2. Defining Configuration Details**"""
def process_sudoku(image_path, paths):

    # 2. DEFINING CONFIGURATION DETAILS
    path_image = image_path
    # path_image = image_path
    height_img = 450
    width_img = 450
    model = initialize_prediction_model()  # LOAD THE OCR CNN MODEL

    """**3. Pre-processing the Image**"""

    # 3. PRE-PROCESSING THE IMAGE
    img = cv2.imread(path_image)
    img = cv2.resize(img, (width_img, height_img))  # RESIZE IMAGE TO MAKE IT A SQUARE
    img_blank = np.zeros((height_img, width_img, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING-DEBUGGING IF REQUIRED
    img_threshold = pre_process(img)

    """**4. Find All Contours in the Image**"""

    # 4. FIND ALL CONTOURS IN THE IMAGE
    # from google.colab.patches import cv2_imshow  # USED ONLY IN COLAB
    img_contours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    img_big_contour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    # FIND ALL CONTOURS
    # CONTOUR RETRIEVAL MODE -> WILL DETECT ONLY EXTERNAL CONTOURS (NO CHILD, PARENT, ETC.)
    # CONTOUR APPROXIMATION METHOD -> SIMPLE -> WILL RETAIN ONLY BARE MINIMUM VERTICES
    contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS
    # cv2_imshow(img_contours)
    # cv2.imshow('image contours', img_contours)
    # cv2_imshow(img)
    # cv2.waitKey(0)
    cv2.imwrite(paths[0], img_contours)

    """5.1 Find the Biggest Countour (Sudoku Board)  
    5.2 Split the Sudoku Board Image into smaller images  
    5.3 Extract digits from smaller images
    """

    # 5.1 FIND THE BIGGEST COUNTOUR AND USE IT AS A SUDOKU BOARD
    biggest_contour, max_area = get_biggest_contour(contours) # FIND THE BIGGEST CONTOUR
    # print(biggest_contour)
    # print("Size of the biggest contour: ",biggest_contour.size)
    if biggest_contour.size != 0:
        biggest_contour = reorder(biggest_contour)  # 
        # print(biggest_contour)
        cv2.drawContours(img_big_contour, biggest_contour, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest_contour) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[width_img, 0], [0, height_img],[width_img, height_img]]) # PREPARE POINTS FOR WARP
        transf_matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GET TRANSFORMATION MATRIX
        img_warp_colored = cv2.warpPerspective(img, transf_matrix, (width_img, height_img))  # APPLY PERSPECTIVE TRANSFORMATION TO IMAGE
        img_warp_gray = cv2.cvtColor(img_warp_colored,cv2.COLOR_BGR2GRAY)

        # 5.2. SPLIT THE IMAGE
        img_detected_digits = img_blank.copy()
        img_solved_digits = img_blank.copy()
        boxes = split_boxes(img_warp_gray)
        # print("Len of boxes: ",len(boxes))
        # cv2.imshow("Sample",boxes[65])

        # 5.3 FIND EACH DIGIT AVAILABLE
        numbers = get_prediction(boxes, model)
        # print("predicted boxes: ", numbers)

        # 5.4 DISPLAY THE DETECTED NUMBERS ON THE IMAGE
        img_detected_digits = display_numbers(img_detected_digits, numbers, color=(255, 0, 255))
        numbers = np.asarray(numbers)
        pos_array = np.where(numbers > 0, 0, 1)
        # print("Pos Array: ", pos_array)

        # 6 FIND SOLUTION OF THE SUDOKU BOARD
        board = np.array_split(numbers,9)
        # print("Before solving: " + str(board))
        try:
            # print("Enter try")
            sobj = SudokuSolver.SudokuSolver(board)
            sobj.solve_sudoku()
            # print(sobj.board)
            # print("No Exception")
            #SudokuSolver(board).solve()
        except Exception as e:
            # print("Exception", e)
            pass
        # print("Solved: " + str(board))
        # print("Solved 2: " + str(sobj.board))
        flatlist = []
        for sublist in sobj.board:
            for item in sublist:
                flatlist.append(item)
        solved_numbers = flatlist * pos_array
        img_solved_digits = display_numbers(img_solved_digits,solved_numbers)

        # 7. OVERLAY SOLUTION
        pts2 = np.float32(biggest_contour) # PREPARE POINTS FOR WARP
        pts1 =  np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
        img_inv_warp_colored = img.copy()
        img_inv_warp_colored = cv2.warpPerspective(img_solved_digits, matrix, (width_img, height_img))
        inv_perspective = cv2.addWeighted(img_inv_warp_colored, 1, img, 0.5, 1)
        img_detected_digits = draw_grid(img_detected_digits)
        img_solved_digits = draw_grid(img_solved_digits)
        # cv2_imshow(img_detected_digits)
        # cv2_imshow(img_solved_digits)
        # cv2_imshow(img_inv_warp_colored)
        # cv2_imshow(inv_perspective)
        # cv2.imshow('detected digits',img_detected_digits)
        # cv2.imshow('solved digits', img_solved_digits)
        # cv2.imshow('solved inverted', img_inv_warp_colored)
        # cv2.imshow('solution', inv_perspective)
        cv2.imwrite(paths[1], img_detected_digits)
        cv2.imwrite(paths[2], img_solved_digits)
        cv2.imwrite(paths[3], inv_perspective)
        # print(paths)
        # print(image_path)
        # image_array = ([img,img_threshold,img_contours, img_big_contour],
        #             [img_detected_digits, img_solved_digits,img_inv_warp_colored,inv_perspective])
        # stacked_image = stack_images(image_array, 1)
        # cv2.imshow('Stacked Images', stacked_image)
        if any(solved_numbers):
            return 'Success'
        else:
            return 'Sudoku Solution Not Found'
    else:
        # print("No Sudoku Found")
        return 'Sudoku Puzzle Not Identified    '
        

    # cv2.waitKey(0)
