import imutils
from os import listdir
from os.path import isfile, join
import numpy as np
from matplotlib import pyplot as plt
from joblib import load
from LocalBinaryPattern import LocalBinaryPatterns
import cv2

# Detection using pre trained model
def binClassifier(input_image):
    decoding = {
        0: "Non banana",
        1: "Banana"
    }
    radius = 3
    no_points = 8 * radius
    desc = LocalBinaryPatterns(no_points, radius)
    image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(image)
    hist = np.array(hist)
    model = load('../Detecting banano/classifier.joblib')
    prediction = model.predict(hist.reshape(1, -1))
    print("Prediction: ", decoding[prediction[0]])
    return prediction

# ---------------- Finding Object to crop it -----------------------------
def colorMask(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gray', gray)
    #cv2.waitKey(0)

    kernel = np.ones((6, 6), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY)
    #cv2.imshow('Mask', thresh)
    #cv2.waitKey(0)

    cnts, hierarchy= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #contourned = cv2.drawContours(img, cnts, 1, (0,255,0), 1)
    #cv2.imshow('Contourned', img)
    #cv2.waitKey(0)

    out = np.zeros_like(img) # Extract out the object and place into output image
    out[thresh == 0] = img[thresh == 0]
    #cv2.imshow('Cropped', out)
    #cv2.waitKey(0)

    #cv2.destroyAllWindows()
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

def main(sourcepath, outputpath):
    print(outputpath)
    #cv2.namedWindow('Entrada', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('Entrada', 450,450)
    #cv2.imshow("Entrada", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    onlyfiles = [f for f in listdir(sourcepath) if(isfile(join(sourcepath, f)))]
    count = 0
    for i, files in enumerate(onlyfiles):
        if(".jpg" in onlyfiles[i]):
            image_path = sourcepath + files
            #print("{0} => {1}".format(i, image_path))

            img = cv2.imread(image_path)
            img = cv2.resize(img, (150, 150))

            if(img is None):
                print('Could not open or find the images')
                exit(0)

            detector = binClassifier(img.copy())
            if(detector):
                out = colorMask(img)
                cv2.imwrite(outputpath + str(count) + ".jpg" , out)
                #hist = histogram(out)
                #print("Valores del histograma RGB: ", hist)
                #hog_result = hog(out)
                #print("HOG shape: {0}| HOG type: {1}".format(hog_result.shape, type(hog_result)))
                count += 1
                
            else:
                print("No se han encontrado similitudes")
                print("pasando al siguiente...")
        print("siguiente imagen...")
    print("finalizado, dataset limpio")

main('../Captured images/Second Try Dataset (green banana)/', './Cleared images/Green banana/')
main('../Captured images/Third Try Dataset (green segment)/', './Cleared images/Green segment/')
main('../Captured images/Fifth Try (green segment without ventilation)/', './Cleared images/Green segment (no ventilation)/')


