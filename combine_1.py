#coding=utf-8
import numpy as np
import cv2
from glob import glob

def combine_movie():

    # 入力する動画と出力パスを指定。
    N = len(glob("*.avi"))
    result = "combined_movie.avi" 
    print "Total movie is", N
    # 形式はMP4Vを指定
    fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
    fps    = 100
    height = 768
    width  = 1024
    print(fps, int(width), int(height))
    
    # 出力先のファイルを開く(s=2;fast,s=0.5;slow)
    s=1
    out = cv2.VideoWriter(result, int(fourcc), int(fps*s), (int(width), int(height)))
    # 動画の読み込みと動画情報の取得
    # for i in range(1,3):
    #     if i==1:
    #         movie = cv2.VideoCapture(target1[0])
    #         print(i)
    #     elif i==2:
    #         movie = cv2.VideoCapture(target2[0])
    #         print(i)
        
    #     # 最初の1フレームを読み込む
    #     if movie.isOpened() == True:
    #         ret,frame = movie.read()
    #     else:
    #         ret = False

    #     # フレームの読み込みに成功している間フレームを書き出し続ける
    #     while ret:
            
    #         # 読み込んだフレームを書き込み
    #         out.write(frame)

    #         # 次のフレームを読み込み
    #         ret,frame = movie.read()
    for fn in range(N):
        # if i==1:
        #     movie = cv2.VideoCapture(target1[0])
        #     print(i)
        # elif i==2:
        #     movie = cv2.VideoCapture(target2[0])
        #     print(i)
        movie = cv2.VideoCapture(glob("*" + str(fn) + ".avi")[0])
        print "loading..." , movie
        
        # 最初の1フレームを読み込む
        if movie.isOpened() == True:
            ret,frame = movie.read()
        else:
            ret = False

        # フレームの読み込みに成功している間フレームを書き出し続ける
        while ret:
            
            # 読み込んだフレームを書き込み
            out.write(frame)

            # 次のフレームを読み込み
            ret,frame = movie.read()
    print "Finish!!"
            


if __name__ == '__main__':
    combine_movie()