# Color picker for HSV range system

import cv2 ,imutils
import numpy as np
import pandas as pd

image_hsv = None
image_rgb = None
count = 0
pixelRGB = [] #RANDOM DEFAULT VALUE
pixelHSV = [] #RANDOM DEFAULT VALUE


index=["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

clicked = False
r = g = b = xpos = ypos = 0

def recognize_color(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        # set the boundary for hue
        boundary = 180
    elif ranges == 1:
        # set the boundary for saturation and value
        boundary = 255

    boundary = 255 if ranges else 180
    value = value+tolerance if upper_or_lower else value-tolerance

    if value > boundary:
        value = boundary
    if value < 0:
        value = 0

    return value

def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b,g,r,xpos,ypos, clicked,count
        global image_rgb,image_hsv

        pixelRGB = image_rgb[y,x]
        pixelHSV = image_hsv[y,x]
        r,g,b = int(pixelRGB[0]),int(pixelRGB[1]),int(pixelRGB[2])
        xpos, ypos = x, y
        clicked = True
        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
        # Set range = 0 for hue and range = 1 for saturation and brightness
        # set upper_or_lower = 1 for upper and upper_or_lower = 0 for lower
        Hue_upper = check_boundaries(pixelHSV[0], 10, 0, 1)
        Hue_lower = check_boundaries(pixelHSV[0], 10, 0, 0)
        Satuation_upper = check_boundaries(pixelHSV[1], 10, 1, 1)
        Satuation_lower = check_boundaries(pixelHSV[1], 10, 1, 0)
        Value_upper = check_boundaries(pixelHSV[2], 20, 1, 1)
        Value_lower = check_boundaries(pixelHSV[2], 20, 1, 0)

        upper =  np.array([Hue_upper, Satuation_upper, Value_upper])
        lower =  np.array([Hue_lower, Satuation_lower, Value_lower])
        ptxt = f"point({x},{y}),RGB({pixelRGB[0]},{pixelRGB[1]},{pixelRGB[2]}),HSV({pixelHSV[0]},{pixelHSV[1]},{pixelHSV[2]}),lower_HSV{lower},upper_HSV{upper}"
        print(ptxt)

        #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS 
        image_mask = cv2.inRange(image_hsv,lower,upper)
        count = int(image_mask.sum()/255)
        cv2.imshow("Mask",image_mask)

        '''

        contours, hierarchy = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            cont = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(cont)
            
            M = cv2.moments(cont)
            if(M["m00"] != 0):
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                area = M["m00"]
                cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.circle(image,(cx,cy),5,(255,255,255),-1)
                cv2.putText(image,f"area({area})",(cx+5,cy+5),1,0.8,(0,255,255),1)
                cv2.drawContours(image,[cont],0,(255,255,255),3)

        '''      
def main(file_path):

    global image_rgb,image_hsv
    global b,g,r,xpos,ypos, clicked
    
    image_src = cv2.imread(file_path)
    image_src = cv2.medianBlur(image_src,3)
    image_src = imutils.resize(image_src,height=700)

    image_rgb = cv2.cvtColor(image_src,cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)

    # cv2.namedWindow("RGB")
    image_bgr = image_src.copy()

    while True :
        cv2.imshow("RGB",image_bgr)
        #CREATE THE HSV FROM THE BGR IMAGE
        cv2.imshow("HSV",image_hsv)
        #CALLBACK FUNCTION
        cv2.setMouseCallback("RGB", pick_color)
 
        if clicked :
            cv2.rectangle(image_bgr,(0,20),(image_bgr.shape[1],60),(b,g,r),-1)
            #Creating text string to display( Color name and RGB values )
            text = recognize_color(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b) + ' cnt= '+str(count)
            #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
            cv2.putText(image_bgr, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
            #For very light colours we will display text in black colour
            if(r+g+b>=600):
                cv2.putText(image_bgr, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

            # cv2.imshow("RGB",image_src)  
            clicked=False

        if cv2.waitKey(10) & 0xFF ==ord('q'):
            break
    cv2.destroyAllWindows()

if __name__=='__main__':
    file_path = "croped/light_blue.jpg"
    main(file_path)