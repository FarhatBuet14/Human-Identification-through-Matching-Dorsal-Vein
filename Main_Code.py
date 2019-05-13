import numpy as np
import imutils
import cv2


def get_accumEdged(image):
    accumEdged = np.zeros(image.shape[:2], dtype="uint8")

    # loop over the blue, green, and red channels, respectively
    for chan in cv2.split(image):
        chan = cv2.medianBlur(chan, 3)
        edged = cv2.Canny(chan, 150, 200)
        accumEdged = cv2.bitwise_or(accumEdged, edged)
            
    cv2.imshow("Edge Map", accumEdged)
    
    while True:    
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            break
        
    return accumEdged




def find_contour_needed(accumEdged):
    
    contour_image = accumEdged
    
    cnts = cv2.findContours(contour_image, cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    cnts_nedded = []
    area = []
    for c in cnts:
        if(cv2.contourArea(c) > 100):
            area.append(cv2.contourArea(c))
            cnts_nedded.append(c)

    return cnts_nedded




def get_point_value(accumEdged):
    points_value = []
    for x in range(0, accumEdged.shape[1]):
        points_value.append(accumEdged[(accumEdged.shape[0]-10), x])   
    
    indexes = [i for i, x in enumerate(points_value) if x == 255]
    
    return indexes


def find_definite_indexes(indexes):
    start_bool = False
    end_bool = False
    definite_index = []
    start = 0
    end = 0
    
    for arg_index in range(0, len(indexes)):   
        
        if((arg_index == 0) & (end_bool == False) & (start_bool == False)): 
            ##########   First Value   #########
            #print("first  - " + str(indexes[arg_index]))
            
            if(len(indexes) > 1):  #More than one index
                #print("More than one index "+ str(indexes[arg_index]))
                diff_after = indexes[arg_index + 1] - indexes[arg_index]
                
                if((diff_after > 5) & (end_bool == False) & (start_bool == False)): #One Point
                    #print("one point + first  - " + str(indexes[arg_index]))
                    definite_index.append(indexes[arg_index])
                    start = 0
                    end = 0
                    end_bool = False
                    start_bool = False
                else:  #point with more than one
                    start = indexes[arg_index]
                    start_bool = True
                    
            else:  # one index + First Value
                #print("Just a single array - " + str(indexes[arg_index]))
                definite_index.append(indexes[arg_index])
                start = 0
                end = 0
                end_bool = False
                start_bool = False
                break
        
        elif(indexes[arg_index] == indexes[-1]):
            ##########   Last Value   #########
            #print("last   - " + str(indexes[arg_index]))
            
            diff_after = indexes[arg_index] - indexes[arg_index - 1]
            
            if((diff_after > 5) & (end_bool == False) & (start_bool == False)): #One Point
                #print("one point + last  - " + str(indexes[arg_index]))
                definite_index.append(indexes[arg_index])
                start = 0
                end = 0
                end_bool = False
                start_bool = False
            else:  #point with more than one
                end = indexes[arg_index]
                end_bool = True
                definite_index.append(int((start+end)/2))
        
        
        else:  
            ##########   Middle Value   #########
            #print("Middle   - " + str(indexes[arg_index]))
            diff_bef = indexes[arg_index] - indexes[arg_index - 1]
            diff_after = indexes[arg_index + 1] - indexes[arg_index]
            
            if((diff_bef > 5) & (diff_after < 5) & (end_bool == False) & (start_bool == False)):
                #print("start (Middle) - " + str(indexes[arg_index]))
                start = indexes[arg_index]
                start_bool = True
            
            elif((diff_bef < 5 ) & (diff_after > 5) & (end_bool == False) & (start_bool == True)):  
                #print("end (Middle)  - " + str(indexes[arg_index]))
                end = indexes[arg_index]
                definite_index.append(int((start+end)/2))
                start = 0
                end = 0
                end_bool = False
                start_bool = False
            
            elif((diff_bef > 5 ) & (diff_after > 5) & (end_bool == False) & (start_bool == False)):  
                #print("one point (Middle)  - " + str(indexes[arg_index]))
                definite_index.append(indexes[arg_index])
                start = 0
                end = 0
                end_bool = False
                start_bool = False

    return definite_index




def find_middle_point(image_name, definite_index, accumEdged):
    if(len(definite_index) > 0):
        point = [(accumEdged.shape[0]-10), int(sum(definite_index)/len(definite_index))]
        
        print(image_name + " === " 
              + str(len(definite_index)) + "   ---  (done) ")
    
        
        orig = image.copy()
        cv2.circle(orig, (point[1], point[0]), 5, (0, 255, 0), -1)
        
        cv2.imshow("Middle point", orig)
    
        while True:    
            key = cv2.waitKey(1)
            if key == 27:
                cv2.destroyAllWindows()
                break
    
        
    
        orig = image.copy()
        for i in range(0, len(definite_index)):
            cv2.circle(orig, (definite_index[i], (accumEdged.shape[0]-10)), 5, (0, 255, 0), -1)
    
        cv2.imshow("points", orig)
        
        while True:    
            key = cv2.waitKey(1)
            if key == 27:
                cv2.destroyAllWindows()
                break
    
    else:
        print(image_name + " ===  " + str(len(definite_index)))
    
    return point



def middle_point_from_image(image_name, accumEdged):

    indexes = get_point_value(accumEdged)
    
    definite_index = find_definite_indexes(indexes)
    
    middle_pont = find_middle_point(image_name, definite_index, accumEdged)

    return middle_pont




############## Main Code ############

total_samples = 5

folder_path = "./HandVeinDatabase/left - 1200/act - 300/"

k = 1
for i in range(1, int(total_samples/2)+1):
    for j in range(1, 4):
        # load the image, clone it, and setup the mouse callback function
        image_name = "p" + str(i) + "_left_act_" + str(j) + ".bmp"
        image = cv2.imread(folder_path + image_name)
        accumEdged = get_accumEdged(image)
        cnts_nedded = find_contour_needed(accumEdged)
        middle_point = middle_point_from_image(image_name, accumEdged)
        
      

