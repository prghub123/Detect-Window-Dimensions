from cv2 import cv2 
import numpy as np 
import matplotlib.pyplot as plt 

# Finds height and width of rectangle given set of four lines 
# Params: Set of Lines (List of 2 endpoints) 
# Return Width, Height of Rectangle 
def find_pixel_dimensions(lines):
    width_lines = []
    height_lines = [] 

    # if no lines were found just return 0 for both width and height 
    if lines is None:
        return 0, 0

    #iterate through all the found lines (should be set of 4) 
    for line in lines:
        # check if vertical line (x coordinate is the same) 
        if line[0][0] == line[0][2]:
            width_lines.append(line)
        #check if horizontal line (y coordinate is the same)  
        elif line[0][1] == line[0][3]:
            height_lines.append(line) 

    # calculate width by finding pixel difference between x coordinates on vertical lines 
    width = abs(width_lines[0][0][0] - width_lines[1][0][0])

    # calculate height by finding pixel difference between y coordinates on horizontal lines 
    height = abs(height_lines[0][0][1] - height_lines[1][0][1])

    return width, height 

# Samples the Boundary of the rectangle based on the reference object and forms a set of points outlining the rectangle
# Params: 
def outline_shape():
    return 

# Translates Pixel Distances to Real Distance Measurements given reference object dimensions
# Uses Simple Ratio Technique to extrapolate dimensions 
# Note: Reference object constant as Circle (Diameter needs to be given); Give real measurement in millimeters 
# Params: reference object diameter, reference object diameter in pixels, Rectangle width in pixels, Rectangle height in pixels 
def find_real_dimensions(reference_real_diameter, reference_pixel_diameter, pixel_width, pixel_height):
    mm_per_pixel = reference_real_diameter / reference_pixel_diameter 
    real_width = pixel_width * mm_per_pixel
    real_height = pixel_height * mm_per_pixel
    return real_width, real_height 

# -----------------------------------------------------
# MAIN RUNNING CODE HERE 
# ----------------------------------------------------- 

REFERENCE_DIAMETER = float(input("What is the diameter of the reference object? Please enter value in millimeters (mm): "))


# load in image and convert it to grayscale 
img = cv2.imread('circleRectangle.jpg', cv2.IMREAD_COLOR)
"""
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
""" 
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# perform canny edge detection on image 
# Note: 2nd argument - minVal; 3rd argument - maxVal for thresholding edges 
edge_img = cv2.Canny(gray_img, 50, 200) 

# ------- Detecting Rectangle Shape -------

# finds straight lines in image using Probablistic Hough Line Transform
# Note: 5th argument - minLineLength; 6th argument - maxLineGap  
lines = cv2.HoughLinesP(edge_img, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
#print(lines) 

#makes copy of original image to project lines 
lines_img = img.copy() 

# highlights the straight lines on the new version of the image 
if lines is not None:
    for line in lines:
        print(line) 
        # extracts both (x,y) coordinates of each endpoint and calls cv2.line() method 
        cv2.line(lines_img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (120, 130, 60), thickness=10)

rect_width, rect_height = find_pixel_dimensions(lines)
 

# ------ Detecting Reference Circle ------ 
rect_actual_width = 0
rect_actual_height = 0 

# copying gray image to use for circle detection 
circle_gray_img = gray_img.copy() 

# Finds circles in image using HOUGH GRADIENT METHOD
# Internally passing in image through canny edge detector so passing in gray image as image parameter 
circles = cv2.HoughCircles(circle_gray_img, cv2.HOUGH_GRADIENT, 1.2, 100, param1=200, param2=100, minRadius=0, maxRadius=0)

# check if any circles are actually found 
if circles is not None:
    #round to integers for pixel calculation and drawing 
    circles_rounded = np.uint8(np.around(circles))

    # if more than one circle found, calibration did not work as intended 
    if len(circles_rounded[0,:]) > 1:
        print("More than one reference object found! Please try detecting image again.")
    
    else:
        # extract x,y coordinates and radius to draw circle and center of circle 
        for i in circles_rounded[0,:]:
            #print(f"x: {i[0]}, y: {i[1]}, radius: {i[2]}")
            # draw actual circle 
            cv2.circle(circle_gray_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw center of circle 
            cv2.circle(circle_gray_img, (i[0], i[1]), 2, (0, 160, 0), 2) 
            # calculate real dimensions of rectangle given coordinates of reference object 
            rect_actual_width, rect_actual_height = find_real_dimensions(REFERENCE_DIAMETER, 2 * i[2], rect_width, rect_height) 

else:
    print("Reference object cannot be found! Please try again.")


print(f"Rectangle Width: {rect_actual_width} mm Rectangle Height: {rect_actual_height} mm")

# show rectangle line image on screen 
cv2.imshow('line image', lines_img)
cv2.waitKey(0)
cv2.destroyAllWindows() 

# show reference circle on screen 
cv2.imshow("reference circle", circle_gray_img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
