from glob import glob
import os
import cv2
j=0

new_dir_path = './png_file/'
os.mkdir(new_dir_path)

A = glob('combined_movie.avi')
print (A[0])

cap = cv2.VideoCapture(A[0])
while(cap.isOpened()):
    flag, frame =cap.read()
    if flag == False:
        break
    cv2.imwrite(new_dir_path + str(j)+'.png', frame)

#for i in range(N):
#    A=[j,j+1,j+2]
#    print "left"+'{0:04}'.format(i)+".png"
    #writer = csv.writer(f, lineterminator='\n')
    #writer.writerow(A)
    
    print j
    j=j+1
