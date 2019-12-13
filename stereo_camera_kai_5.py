# -*- coding: utf-8 -*-

import numpy
import cv2
import csv
import datetime
import glob
import re

now = datetime.datetime.now()
date = '{0:%m_%d_%H-%M-%S}'.format(now)
f= open('Position_measurement' + date + ".csv",'w')

N = 1900
imageSize = (1024,768)
# j = 711 #L
# k = 584 #R
thresh = 240
#thresh = 100
mac_pixel =255
directory_left  = './left_movie/png_file/'
directory_right = './right_movie/png_file/'
dorectory_calibration = './calibration/'

list_left = glob.glob(directory_left + '*.png')
list_right = glob.glob(directory_right + '*.png')

p = re.compile(r'\d+')
list_left_sort = sorted(list_left, key=lambda s: int(p.search(s).group()))
list_right_sort = sorted(list_right, key=lambda s: int(p.search(s).group()))

cameraMatrix1 = numpy.loadtxt(dorectory_calibration + 'cameraMatrix1.csv',delimiter = ',')
cameraMatrix2 = numpy.loadtxt(dorectory_calibration + 'cameraMatrix2.csv',delimiter = ',')
distCoeffs1 = numpy.loadtxt(dorectory_calibration + 'distCoeffs1.csv',delimiter = ',')
distCoeffs2 = numpy.loadtxt(dorectory_calibration + 'distCoeffs2.csv',delimiter = ',')
R = numpy.loadtxt(dorectory_calibration + 'R.csv',delimiter = ',')
T = numpy.loadtxt(dorectory_calibration + 'T.csv',delimiter = ',')

# 平行化変換のためのRとPおよび3次元変換行列Qを求める
flags = 0
alpha = 1
newimageSize = (1024,768)
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T, flags, alpha, newimageSize)

# 平行化変換マップを求める
m1type = cv2.CV_32FC1
map1_l, map2_l = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, P1, newimageSize, m1type) #m1type省略不可
map1_r, map2_r = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2, P2, newimageSize, m1type)





def calculate_contour_area(im_l,im_r):
    interpolation = cv2.INTER_NEAREST
    Re_TgtImg_l = cv2.remap(im_l, map1_l, map2_l, interpolation)
    Re_TgtImg_r = cv2.remap(im_r, map1_r, map2_r, interpolation)

    img_gray_l = cv2.cvtColor(Re_TgtImg_l, cv2.COLOR_BGR2GRAY)
    img_gray_r = cv2.cvtColor(Re_TgtImg_r, cv2.COLOR_BGR2GRAY)

    thresh = 240
    mac_pixel =255

    ret_l,img_l =cv2.threshold(img_gray_l, thresh , mac_pixel,cv2.THRESH_BINARY)
    ret_l,img_r =cv2.threshold(img_gray_r, thresh , mac_pixel,cv2.THRESH_BINARY)

    M_l = cv2.moments(img_l)
    M_r = cv2.moments(img_r)

    return M_l['m00'],M_r['m00']

def calculate_moment_left(j):
    im_l = cv2.imread(list_left_sort[j])
    print list_left_sort[j] 

    interpolation = cv2.INTER_NEAREST
    Re_TgtImg = cv2.remap(im_l, map1_l, map2_l, interpolation)
    img_gray = cv2.cvtColor(Re_TgtImg, cv2.COLOR_BGR2GRAY)
    ret,img =cv2.threshold(img_gray, thresh , mac_pixel,cv2.THRESH_BINARY)
    M = cv2.moments(img)
    #cv2.imwrite('./test_gray/' + 'test_' + str(j) + '.jpg', Re_TgtImg)
    #print (M)
    return M

def calculate_moment_right(k):
    im_r = cv2.imread(list_right_sort[k])
    print  list_right_sort[k] 

    interpolation = cv2.INTER_NEAREST
    Re_TgtImg = cv2.remap(im_r, map1_r, map2_r, interpolation)
    img_gray = cv2.cvtColor(Re_TgtImg, cv2.COLOR_BGR2GRAY)
    ret,img =cv2.threshold(img_gray, thresh , mac_pixel,cv2.THRESH_BINARY)
    M = cv2.moments(img)
    return M

def aaa(M_l,M_r):
    cx_l = M_l['m10']/M_l['m00']#-495.3160
    cx_r = M_r['m10']/M_r['m00']#-505.7374
    cy_l = M_l['m01']/M_l['m00']
    d_x = cx_l - cx_r

    m = [[cx_l],[cy_l],[d_x],[1]]
    B = Q.dot(m)
    A = [B[0][0]/B[3][0] , B[1][0]/B[3][0] , B[2][0]/B[3][0]]
    return A


def find_first():
    j = 0
    k = 0
    while True:
        moment_l = calculate_moment_left(j)
        area_l = moment_l['m00']
        
        while True:
            if area_l == 0:
                j = j + 1
                moment_l = calculate_moment_left(j)
                area_l = moment_l['m00']
                continue
            
            if area_l > 0:
                print "Found left"
                j_0 = j
                break


        moment_r = calculate_moment_right(k)
        area_r = moment_r['m00']

        while True:
            if area_r == 0:
                k = k + 1
                moment_r = calculate_moment_right(k)
                area_r = moment_r['m00']
                

            if area_r > 0:
                print "Found right"
                k_0 = k
                break

        print (j_0,k_0)
        return j_0,k_0
        break


def loop_main():
    first = find_first()
    j = first[0]
    k = first[1]

    moment_l = calculate_moment_left(j)
    area_l = moment_l['m00']
    moment_r = calculate_moment_right(k)
    area_r = moment_r['m00']
    A0 = aaa(moment_l,moment_r)

    while True:
        moment_l = calculate_moment_left(j)
        area_l = moment_l['m00']

        moment_r = calculate_moment_right(k)
        area_r = moment_r['m00']
        
        if area_l > 0 and area_r > 0:
            A = aaa(moment_l,moment_r)
            A = [A[0] - A0[0],A[1] - A0[1],A[2] - A0[2]]
            j = j + 1
            k = k + 1

            writer = csv.writer(f,lineterminator = '\n')
            writer.writerow(A)
            

        if area_l == 0 or area_r == 0:
            break
        
        if j == (len(list_left_sort) - 1) or k == (len(list_right_sort) - 1):
            break

    


    print("Finish")

    
if __name__ == "__main__":
    print "Start!!"
    loop_main()
    


            

        
        