# Color check for RGB range
# Required moduls
import cv2 ,imutils
import numpy as np
import sys

# color RGB range
min_black = np.array([0,0,0],np.uint8)
max_black = np.array([28,29,34],np.uint8)

min_green = np.array([10, 65, 62],np.uint8)
max_green = np.array([30,85,82],np.uint8) 

min_lggreen = np.array([58, 73,32],np.uint8)
max_lggreen = np.array([78,96,52],np.uint8) 

min_dkgreen = np.array([5, 11, 14],np.uint8)
max_dkgreen = np.array([25,31,34],np.uint8) 

min_dkblue = np.array([11, 20, 59],np.uint8)
max_dkblue = np.array([31, 40, 79],np.uint8)

min_lgblue = np.array([17, 61,86],np.uint8)
max_lgblue = np.array([37, 81, 106],np.uint8)

min_blue = np.array([0, 36, 78],np.uint8)
max_blue = np.array([19, 56, 98],np.uint8)

min_pink = np.array([100,54,91],np.uint8)
max_pink = np.array([120,74,111],np.uint8)

min_lgpink = np.array([98,70,93],np.uint8)
max_lgpink = np.array([118,90,113],np.uint8)

min_violet = np.array([43,34,81],np.uint8)
max_violet = np.array([63,54,101],np.uint8)

name = ""

colors = {"lightpink":[min_lgpink,max_lgpink],"pink":[min_pink,max_pink],"violet":[min_violet,max_violet],
          "lightgreen":[min_lggreen,max_lggreen],"green":[min_green,max_green],"darkgreen":[min_dkgreen,max_dkgreen],
          "lightblue":[min_lgblue,max_lgblue],"blue":[min_blue,max_blue],"darkblue":[min_dkblue,max_dkblue],
          "black":[min_black,max_black]}


font = cv2.FONT_HERSHEY_SIMPLEX

sourceImage = cv2.imread("croped/light_green.jpg")
sourceImage = imutils.resize(sourceImage,height=700)
sourceImage = cv2.medianBlur(sourceImage,5)

# Convert image to YCrCb
imageRGB = cv2.cvtColor(sourceImage,cv2.COLOR_BGR2RGB)

# Find region with skin tone in YCrCb image
max = 0
for color in colors:

    maskRegion = cv2.inRange(imageRGB,colors[color][0],colors[color][1])
    count = int((maskRegion.sum())/255)
    if count > max :
        max = count
        name = color
print("Color = ",name ,"and Count = ",max)
maxRegion = cv2.inRange(imageRGB,colors[name][0],colors[name][1])

# sys.exit()
cv2.imshow('region',maxRegion)

rgb = colors[name][1]-10
# sys.exit()
cv2.rectangle(sourceImage,(0,20),(sourceImage.shape[1],60),(int(rgb[2]),int(rgb[1]),int(rgb[0])),-1)
cv2.putText(sourceImage,f"Color is ({name}) and Count = {max}",(30,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
cv2.imshow('Detect Color',sourceImage)

cv2.waitKey(0) 
# Close window and camera after exiting the while loop
cv2.destroyAllWindows()
