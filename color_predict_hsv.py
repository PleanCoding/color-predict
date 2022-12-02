# Color check for HSV range
# Required moduls
import cv2 ,imutils
import numpy as np
import sys

# color HSV range
min_black = np.array([100,55,0],np.uint8)
max_black = np.array([124,85,37],np.uint8)

min_green = np.array([78, 174, 50],np.uint8)
max_green = np.array([99,216,96],np.uint8) 

min_lggreen = np.array([31, 116,56],np.uint8)
max_lggreen = np.array([53,146,96],np.uint8) 

min_dkgreen = np.array([99, 93, 0],np.uint8)
max_dkgreen = np.array([119,113,40],np.uint8) 

min_blue = np.array([98, 232, 57],np.uint8)
max_blue = np.array([118, 252, 97],np.uint8)

min_lgblue = np.array([91, 185, 73],np.uint8)
max_lgblue = np.array([111, 205, 113],np.uint8)

min_dkblue = np.array([104, 170, 48],np.uint8)
max_dkblue = np.array([124, 190, 88],np.uint8)

min_pink = np.array([147,110,96],np.uint8)
max_pink = np.array([167,145,138],np.uint8)

min_lgpink = np.array([147,38,103],np.uint8)
max_lgpink = np.array([167,58,143],np.uint8)

min_violet = np.array([115,160,55],np.uint8)
max_violet = np.array([135,180,95],np.uint8)

name = ""

colors = {"lightpink":[min_lgpink,max_lgpink],"pink":[min_pink,max_pink],"violet":[min_violet,max_violet],
          "lightgreen":[min_lggreen,max_lggreen],"green":[min_green,max_green],"darkgreen":[min_dkgreen,max_dkgreen],
          "lightblue":[min_lgblue,max_lgblue],"blue":[min_blue,max_blue],"darkblue":[min_dkblue,max_dkblue],
          "black":[min_black,max_black]}


font = cv2.FONT_HERSHEY_SIMPLEX

sourceImage = cv2.imread("croped/dark_green.jpg")
sourceImage = imutils.resize(sourceImage,height=700)
# sourceImage = cv2.medianBlur(sourceImage,5)
# Convert image to YCrCb
imageHSV = cv2.cvtColor(sourceImage,cv2.COLOR_BGR2HSV)

# Find region with skin tone in YCrCb image
max = 0
for color in colors:

    maskRegion = cv2.inRange(imageHSV,colors[color][0],colors[color][1])
    count = int((maskRegion.sum())/255)
    if count > max :
        max = count
        name = color
print("Color = ",name ,"and Count = ",max)
maxRegion = cv2.inRange(imageHSV,colors[name][0],colors[name][1])
# sys.exit()
cv2.imshow('region',maxRegion)
H,S,V = colors[name][1][0]-10, colors[name][1][1]-10, colors[name][1][2]-20
hsv = np.uint8([[[H,S, V]]])
# Convert HSV color to BRG
rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)[0][0]
# sys.exit()
cv2.rectangle(sourceImage,(0,20),(sourceImage.shape[1],60),(int(rgb[2]),int(rgb[1]),int(rgb[0])),-1)
cv2.putText(sourceImage,f"Color is ({name}) and Count = {max}",(30,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
cv2.imshow('Detect Color',sourceImage)

cv2.waitKey(0) 
# Close window and camera after exiting the while loop
cv2.destroyAllWindows()
