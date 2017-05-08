#Achieved Better contrast ,better noise reduction and masking of path
import cv2
import numpy as np

cap = cv2.VideoCapture('./images/video.mp4')

#Defining the kernel size deciding the amount of blur to be applied (Only an odd value will work)
kernel_x=21
kernel_y=21

#Defining Thresholds 
low_threshold=30
high_threshold=200
black_threshold= 240
white_threshold= 250

while True:
    ret,frame= cap.read()
    if ret==True:
        #showing original input
        cv2.imshow("Original",frame)
        #Actual code
        
        #Blurring the floor
        #Making region of interests
        image = np.zeros((frame.shape[0],frame.shape[1],3), np.uint8)
        cv2.rectangle(image, (0,frame.shape[0]/2), (frame.shape[1],frame.shape[0]), (255,255,255), -1)
        gauss_input=cv2.bitwise_and(frame,image)
        
        #Applying Gaussian Filter
        gauss_output=cv2.GaussianBlur(gauss_input,(kernel_x,kernel_y), 0)
        gray1=cv2.cvtColor(gauss_output,cv2.COLOR_BGR2GRAY)
        
        #Applying threshold
        __,threshold1=cv2.threshold(gauss_output,black_threshold,255, cv2.THRESH_TOZERO)
        __,threshold2=cv2.threshold(gauss_output,white_threshold,255, cv2.THRESH_TOZERO_INV)
        cv2.imshow("Thresholded1",threshold1)
        cv2.imshow("Thresholded2",threshold2)
       
        #Combining this into actual image
        frame2=cv2.bitwise_and(threshold1,threshold2)
        cv2.rectangle(frame2, (0,0), (frame.shape[1],frame.shape[0]/2), (255,255,255), -1)
#         cv2.imshow("Thresholded final",frame2)
        frame=cv2.bitwise_and(frame,frame2)
        cv2.imshow("Thresholded final",frame)
        
        #Convert to YUV
        yuv= cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
        Y,U,V= cv2.split(yuv)
        #Histogram Equalization
        cv2.equalizeHist(Y,Y)
        equalized=cv2.merge([Y,U,V])
#         cv2.imshow("New",equalized)
        
        #Convert back to color
        colored=cv2.cvtColor(equalized,cv2.COLOR_YUV2BGR)
        
        #Making region of interests
        image2 = np.zeros((colored.shape[0],colored.shape[1],3), np.uint8)
        cv2.rectangle(image2, (0,colored.shape[0]/2-200), (colored.shape[1],colored.shape[0]/2-20), (255,255,255), -1)
        rectImg=cv2.bitwise_and(colored,image2)
        
        canny1= cv2.Canny(colored, low_threshold, high_threshold)
        cv2.imshow("Canny1", canny1)
        
#         contours=cv2.contourArea()
        
#         circ= cv2.circle(colored, (350, 350), 100, (15,75,50), 1)
#         circImg=cv2.bitwise_xor(colored,colored, mask=circ)
        
#         canny2= cv2.Canny(circImg, low_threshold, high_threshold)
#         cv2.imshow("Canny2", circImg)
        
#         cv2.imshow("Colored",rectImg)
#         Mat img;
#         Rect rect;
#         /* Get the img from webcam or from file. Get points from mousecallback
#          * or define the points
#          */
#         rect = Rect(point1.x,point1.y,point2.x-point1.x,point2.-point1.y);
#         Mat roiImg;
#         roiImg = img(rect); /* sliced image */

#         #Convert to YUV
#         yuv2= cv2.cvtColor(colored,cv2.COLOR_BGR2YUV)
#         Y2,U2,V2= cv2.split(yuv2)
#         #Histogram Equalization
#         cv2.equalizeHist(Y2,Y2)
#         equalized2=cv2.merge([Y2,U2,V2])
# #         cv2.imshow("New",equalized)
        
#         #Convert back to color
#         colored2=cv2.cvtColor(equalized2,cv2.COLOR_YUV2BGR)
#         cv2.imshow("Colored2",colored2)
        
        if cv2.waitKey(1) == 32:
            while True:
                if cv2.waitKey(1)== 32:
                    break
        if cv2.waitKey(30) & 0xFF == ord('q'):
                break
    else:
        break
cap.release()
cv2.destroyAllWindows()
            