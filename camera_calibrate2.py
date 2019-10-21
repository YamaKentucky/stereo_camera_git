# -*- coding: utf-8 -*-

import numpy
import cv2
from glob import glob
import Tkinter
import tkMessageBox


def main():

    square_size = 95      # 正方形のサイズ
    pattern_size = (10, 7)  # 模様のサイズ
    pattern_points = numpy.zeros( (numpy.prod(pattern_size), 3), numpy.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points[:,:2] = numpy.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []

    for fn in glob("left*.jpg"):
        # 画像の取得
        im = cv2.imread(fn, 0)
        print "loading..." + fn
        # チェスボードのコーナーを検出
        found, corner = cv2.findChessboardCorners(im, pattern_size)
        # コーナーがあれば
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 100, 0.001)
            cv2.cornerSubPix(im, corner, (5,5), (-1,-1), term)
        # コーナーがない場合のエラー処理
        if not found:
            print 'chessboard not found'
            continue
        img_points.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
        obj_points.append(pattern_points)
        #corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)


    # 内部パラメータを計算
    rms, K_l, d_l, r, t = cv2.calibrateCamera(obj_points,img_points,(im.shape[1],im.shape[0]))
    # 計算結果を表示
    print "RMS = ", rms
    print "K = \n", K_l
    print "d = ", d_l.ravel()
    # 計算結果を保存
    numpy.savetxt("K_left.csv", K_l, delimiter =',',fmt="%0.14f") #カメラ行列の保存
    numpy.savetxt("d_left.csv", d_l, delimiter =',',fmt="%0.14f") #歪み係数の保存

    obj_points = []
    img_points = []

    for fn in glob("right*.jpg"):
        # 画像の取得
        im = cv2.imread(fn, 0)
        print "loading..." + fn
        # チェスボードのコーナーを検出
        found, corner = cv2.findChessboardCorners(im, pattern_size)
        # コーナーがあれば
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 100, 0.001)
            cv2.cornerSubPix(im, corner, (5,5), (-1,-1), term)
        # コーナーがない場合のエラー処理
        if not found:
            print 'chessboard not found'
            continue
        img_points.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
        obj_points.append(pattern_points)
        #corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)


    # 内部パラメータを計算
    rms, K_r, d_r, r, t = cv2.calibrateCamera(obj_points,img_points,(im.shape[1],im.shape[0]))
    # 計算結果を表示
    print "RMS = ", rms
    print "K = \n", K_r
    print "d = ", d_r.ravel()
    # 計算結果を保存
    numpy.savetxt("K_right.csv", K_r, delimiter =',',fmt="%0.14f") #カメラ行列の保存
    numpy.savetxt("d_right.csv", d_r, delimiter =',',fmt="%0.14f") #歪み係数の保存

    #N = 24 #キャリブレーション用ステレオ画像のペア数
#　　　　「left0.jgp」のように、ペア番号を'left','right'の後につけて同じフォルダに置く(grobが使いこなせれば直したい)
    N = len(glob("right*.jpg"))

    square_size = 95      # 正方形のサイズ
    pattern_size = (10, 7)  # 模様のサイズ
    pattern_points = numpy.zeros( (numpy.prod(pattern_size), 3), numpy.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points[:,:2] = numpy.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points1 = []
    img_points2 = []


    for i in range(N):
        # 画像の取得
        im_l = cv2.imread("left" +str(i)+ ".jpg", 0)
        im_r = cv2.imread("right" +str(i)+ ".jpg", 0)
        print "loading..." + "left" +str(i)+ ".jpg"
        print "loading..." + "right" +str(i)+ ".jpg"
        #コーナー検出
        found_l, corner_l = cv2.findChessboardCorners(im_l, pattern_size)
        found_r, corner_r = cv2.findChessboardCorners(im_r, pattern_size)
        # コーナーがあれば
        if found_l and found_r:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 100, 0.001)
            cv2.cornerSubPix(im_l, corner_l, (5,5), (-1,-1), term)
            cv2.cornerSubPix(im_r, corner_r, (5,5), (-1,-1), term)
            cv2.drawChessboardCorners(im_l, pattern_size, corner_l,found_l)
            cv2.drawChessboardCorners(im_r, pattern_size, corner_r,found_r)
            #cv2.imshow('found corners in ' + "left" +str(i)+ ".jpg", im_l)
            cv2.imwrite("found_corners_right"+str(i)+".png", im_r)
            cv2.imwrite("found_corners_left"+str(i)+".png", im_l)

        # コーナーがない場合のエラー処理
        if not found_l:
            print 'chessboard not found in leftCamera'
            continue
        if not found_r:
            print 'chessboard not found in rightCamera'
            continue


    img_points1.append(corner_l.reshape(-1, 2))
    img_points2.append(corner_r.reshape(-1, 2))
    obj_points.append(pattern_points)
    print 'found corners in ' + str(i) + ' is adopted'


    # システムの外部パラメータを計算
    imageSize = (im_l.shape[1],im_l.shape[0])
    cameraMatrix1 = K_l
    cameraMatrix2 = K_r
    distCoeffs1 = d_l
    distCoeffs2 = d_r
    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(obj_points, img_points1, img_points2, imageSize, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2)

    # 計算結果を表示
    print "retval = ", retval
    print "R = \n", R
    print "T = \n", T
    # 計算結果を保存
    numpy.savetxt("cameraMatrix1.csv", cameraMatrix1, delimiter =',',fmt="%0.14f") #新しいカメラ行列を保存
    numpy.savetxt("cameraMatrix2.csv", cameraMatrix2, delimiter =',',fmt="%0.14f")
    numpy.savetxt("distCoeffs1.csv", distCoeffs1, delimiter =',',fmt="%0.14f") #新しい歪み係数を保存
    numpy.savetxt("distCoeffs2.csv", distCoeffs2, delimiter =',',fmt="%0.14f")
    numpy.savetxt("R.csv", R, delimiter =',',fmt="%0.14f") #カメラ間回転行列の保存
    numpy.savetxt("T.csv", T, delimiter =',',fmt="%0.14f") #カメラ間並進ベクトルの保存






if __name__ == '__main__':
    main()
