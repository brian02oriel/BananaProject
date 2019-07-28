import cv2
import numpy as np



def ORB_detector(new_image, image_template):
    # Function that compares input image to template
    # It then returns the number of ORB matches between them
    
    image1 = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # Create ORB detector with 1000 keypoints with a scaling pyramid factor of 1.2
    orb = cv2.ORB_create(nfeatures = 1000)

    # Detect keypoints of original image
    (kp1, des1) = orb.detectAndCompute(image1, None)
    template_kp = kp1
    # Detect keypoints of rotated image
    (kp2, des2) = orb.detectAndCompute(image_template, None)
    
    image_template = cv2.drawKeypoints(image_template, kp1, None)
    image1 = cv2.drawKeypoints(image1, kp2, None)
    cv2.imshow("ORB Template Keypoints", image_template)
    cv2.imshow("ORB In Keypoints", image1)
    cv2.waitKey(0)
    # Create matcher 
    # Note we're no longer using Flannbased matching
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Do matching
    matches = bf.match(des1,des2)

    # Sort the matches based on distance.  Least distance
    # is better
    matches = sorted(matches, key=lambda val: val.distance)

    return len(matches), len(kp1)


# Load our image template, this is our reference image
image_template = cv2.imread('images/banano_base.jpeg', 0) 


image1 = cv2.imread('images/banano_v2.jpg') 
if image1 is None or image_template is None:
    print('Could not open or find the images')
    exit(0)

#cv2.imshow("Template", image_template)
#cv2.imshow("In", image1)
#cv2.waitKey(0)

# Get height and width of webcam image1
height, width = image1.shape[:2]

image1 = cv2.flip(image1,1)

 # Define ROI Box Dimensions (Note some of these things should be outside the loop)
top_left_x = width / 3
top_left_y = (height / 2) + (height / 4)
bottom_right_x = (width / 3) * 2
bottom_right_y = (height / 2) - (height / 4)

# Get number of ORB matches 
matches, template_kp = ORB_detector(image1, image_template)

# Display status string showing the current no. of matches 
output_string = "Matches = " + str(matches)
cv2.putText(image1, output_string, (50,450), cv2.FONT_HERSHEY_COMPLEX, 2, (250,0,150), 2)
print(output_string)
# Our threshold to indicate object deteciton
# For new images or lightening conditions you may need to experiment a bit 
# Note: The ORB detector to get the top 1000 matches, 350 is essentially a min 35% match
threshold = template_kp * 35/100
print("Threshold: ", threshold)
    
# If matches exceed our threshold then object has been detected
if matches > threshold:
    cv2.rectangle(image1, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), (0,255,0), 3)
    cv2.putText(image1,'Object Found',(100,100), cv2.FONT_HERSHEY_COMPLEX, 2 ,(0,255,0), 2)
    
cv2.imshow('Object Detector using ORB', image1)
    
cv2.waitKey(0)


cv2.destroyAllWindows()   