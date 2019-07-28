import cv2
import numpy as np


def sift_detector(new_image, image_template):
    # Function that compares input image to template
    # It then returns the number of SIFT matches between them
    
    image1 = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    image2 = image_template
    
    # Create SIFT detector object
    sift = cv2.xfeatures2d.SIFT_create()

    # Obtain the keypoints and descriptors using SIFT
    keypoints_1, descriptors_1 = sift.detectAndCompute(image1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(image2, None)
    
    image_template = cv2.drawKeypoints(image_template, keypoints_2, None)
    image1 = cv2.drawKeypoints(image1, keypoints_1, None)
    cv2.imshow("SIFT Template Keypoints", image_template)
    cv2.imshow("SIFT In Keypoints", image1)
    cv2.waitKey(0)

    # Define parameters for our Flann Matcher
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 3)
    search_params = dict(checks = 100)

    # Create the Flann Matcher object
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Obtain matches using K-Nearest Neighbor Method
    # the result 'matches' is the number of similar matches found in both images
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)

    # Store good matches using Lowe's ratio test
    good_matches = []
    for m,n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m) 

    return len(good_matches)




# Load our image template, this is our reference image
image_template = cv2.imread('images/banano_base.jpeg', 0) 
image1 = cv2.imread('images/alfa.jpg') 

if image1 is None or image_template is None:
    print('Could not open or find the images')
    exit(0)

# Get height and width of webcam image1
height, width = image1.shape[:2]

# Define ROI Box Dimensions
top_left_x = width / 3
top_left_y = (height / 2) + (height / 4)
bottom_right_x = (width / 3) * 2
bottom_right_y = (height / 2) - (height / 4)


    
# Flip image1 orientation horizontally
image1 = cv2.flip(image1,1)
    
# Get number of SIFT matches
matches = sift_detector(image1, image_template)
print("Matches: ", matches)
    
# Our threshold to indicate object deteciton
# We use 10 since the SIFT detector returns little false positves
threshold = 10
    
# If matches exceed our threshold then object has been detected
if matches > threshold:
    cv2.rectangle(image1, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), (0,255,0), 3)
    cv2.putText(image1,'Object Found',(top_left_x + 50 , top_left_y + 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 ,(0,255,0), 2)
    
cv2.imshow('Object Detector using SIFT', image1)
    
cv2.waitKey(0)

cv2.destroyAllWindows()   