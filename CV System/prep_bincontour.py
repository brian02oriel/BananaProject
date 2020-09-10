import imutils
import numpy as np
from matplotlib import pyplot as plt
import cv2

# -------------- ORB detector ----------------
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
    
    cv2.namedWindow('ORB Template Keypoints', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('ORB Template Keypoints', 450,450)
    
    cv2.namedWindow('ORB In Keypoints', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('ORB In Keypoints', 450,450)

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

#--------------- Detection ------------------------------
def formDetection(image1, image_template):
    height, width = image1.shape[:2]

    image1 = cv2.flip(image1,1)

     # Define ROI Box Dimensions (Note some of these things should be outside the loop)
    top_left_x = round(width / 3)
    top_left_y = round((height / 2) + (height / 4))
    bottom_right_x = round((width / 3) * 2)
    bottom_right_y = round((height / 2) - (height / 4))

    # Get number of ORB matches 
    matches, template_kp = ORB_detector(image1, image_template)

    # Display status string showing the current no. of matches 
    output_string = "Matches = " + str(matches)
    cv2.putText(image1, output_string, (top_left_x + 25 , top_left_y + 100), cv2.FONT_HERSHEY_COMPLEX, 1, (250,0,150), 2)
    print(output_string)
    # Our threshold to indicate object deteciton
    # For new images or lightening conditions you may need to experiment a bit 
    # Note: The ORB detector to get the top 1000 matches, 350 is essentially a min 35% match
    threshold = template_kp * 35/100
    #print("Threshold: ", threshold)
    
    # If matches exceed our threshold then object has been detected
    if matches > threshold:
        cv2.namedWindow('Object Detector using ORB', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Object Detector using ORB', 450,450)
        cv2.rectangle(image1, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), (0,255,0), 3)
        cv2.putText(image1,'Object Found',(top_left_x + 50 , top_left_y + 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 ,(0,255,0), 2)
        cv2.imshow('Object Detector using ORB', image1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    else:
        cv2.namedWindow('Object Detector using ORB', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Object Detector using ORB', 450,450)
        cv2.rectangle(image1, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), (0,0,255), 3)
        cv2.putText(image1,'Object Not Found',(top_left_x + 50 , top_left_y + 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 ,(0,0,255), 2)
        cv2.imshow('Object Detector using ORB', image1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return False

# ---------------- Finding Object to crop it -----------------------------
def colorMask(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray', gray)
    cv2.waitKey(0)

    kernel = np.ones((6, 6), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    ret, thresh = cv2.threshold(gray, 245, 255, 0)
    cv2.imshow('Mask', thresh)
    cv2.waitKey(0)

    cnts, hierarchy= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contourned = cv2.drawContours(img, cnts, 1, (0,255,0), 1)
    cv2.imshow('Contourned', img)
    cv2.waitKey(0)

    out = np.zeros_like(img) # Extract out the object and place into output image
    out[thresh == 0] = img[thresh == 0]
    cv2.imshow('Cropped', out)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    return out
#----------------- Histograma RGB -----------------------------
def histogram(img):
    color = ('b', 'g', 'r')
    plt.figure()

    for i, c in enumerate(color):
        hist = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.subplot(221 + i)
        plt.grid(True)
        plt.plot(hist, color = c)
        plt.xlim([0, 256])
    
    plt.show()
    cv2.destroyAllWindows()
    return hist

#------------------------ HOG -------------------------------
def hog(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # h x w in pixels
    cell_size = (8, 8) 

    # h x w in cells
    block_size = (2, 2) 

    # number of orientation bins
    nbins = 9

    # Using OpenCV's HOG Descriptor
    # winSize is the size of the image cropped to a multiple of the cell size
    hog = cv2.HOGDescriptor(_winSize=(gray.shape[1] // cell_size[1] * cell_size[1],
                                  gray.shape[0] // cell_size[0] * cell_size[0]),
                        _blockSize=(block_size[1] * cell_size[1],
                                    block_size[0] * cell_size[0]),
                        _blockStride=(cell_size[1], cell_size[0]),
                        _cellSize=(cell_size[1], cell_size[0]),
                        _nbins=nbins)

    # Create numpy array shape which we use to create hog_feats
    n_cells = (gray.shape[0] // cell_size[0], gray.shape[1] // cell_size[1])

    # We index blocks by rows first.
    # hog_feats now contains the gradient amplitudes for each direction,
    # for each cell of its group for each group. Indexing is by rows then columns.
    hog_feats = hog.compute(gray).reshape(n_cells[1] - block_size[1] + 1,
                            n_cells[0] - block_size[0] + 1,
                            block_size[0], block_size[1], nbins).transpose((1, 0, 2, 3, 4))  

    # Create our gradients array with nbin dimensions to store gradient orientations 
    gradients = np.zeros((n_cells[0], n_cells[1], nbins))

    # Create array of dimensions 
    cell_count = np.full((n_cells[0], n_cells[1], 1), 0, dtype=int)

    # Block Normalization
    for off_y in range(block_size[0]):
        for off_x in range(block_size[1]):
            gradients[off_y:n_cells[0] - block_size[0] + off_y + 1,
                      off_x:n_cells[1] - block_size[1] + off_x + 1] += \
                hog_feats[:, :, off_y, off_x, :]
            cell_count[off_y:n_cells[0] - block_size[0] + off_y + 1,
                       off_x:n_cells[1] - block_size[1] + off_x + 1] += 1

    # Average gradients
    gradients /= cell_count

    # Plot HOGs using Matplotlib
    # angle is 360 / nbins * direction
    color_bins = 5
    plt.pcolor(gradients[:, :, color_bins])
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.colorbar()
    plt.show()
    cv2.destroyAllWindows()
    return gradients


image_template = cv2.imread('../Test images/banano_v2.jpg', 0) 
img = cv2.imread('../Test images/banano_v.jpg')

cv2.namedWindow('Entrada', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Entrada', 450,450)
cv2.imshow("Entrada", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

if img is None or image_template is None:
    print('Could not open or find the images')
    exit(0)

detector = formDetection(img, image_template)
#print("Detector", detector)
if detector:
    out = colorMask(img)
    hist = histogram(out)
    #print("Valores del histograma RGB: ", hist)
    hog = hog(out)
    print("Valores del HOG: ", hog)
    
else:
    print("No se han encontrado similitudes")
    exit(0)
