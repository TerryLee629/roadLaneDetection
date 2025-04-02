import cv2
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
cap = cv2.VideoCapture('LaneVideo.mp4')
out = cv2.VideoWriter('outputMid1212.mp4', fourcc, 30, (640, 400))

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    ww, hh, rh, r = 640, 400, 0.6, 3
    xx1, yy1, xx2, yy2 = int(ww * 0.4), int(hh * rh), int(ww * 0.6), int(hh * rh)
    p1, p2, p3, p4 = [r, hh - r], [ww - 50 , hh -r], [xx2-60, yy2+40], [xx1+60, yy2+40]
    img1 = cv2.resize(frame, (ww, hh))  # 產生 640x400 的圖

    # cv2.imshow('oxxostudio_1', img1)
    # cv2.waitKey(0)
    output = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    # ROI: Region Of Interest (關注區域)
    zero = np.zeros((hh, ww, 1), dtype='uint8')  # ROI
    area = [p1, p2, p3, p4]  # bottom left, bottom right, upper right, upper left
    pts = np.array(area) 
    zone = cv2.fillPoly(zero, [pts], 255)
    output1 = cv2.bitwise_and(output, zone)  # 使用 bitwise_and
    # cv2.imshow('oxxostudio_1', output1)
    # cv2.waitKey(0)
    cv2.imshow('oxxostudio_2', output1)
    cv2.waitKey(1)
    # a1 = np.float32([p4, p3, p1, p2])  # bottom left, bottom right, upper right, upper left
    # a2 = np.float32([[0,0],[ww,0],[0,hh],[ww,hh]])
    a1 = np.float32([p4, p1, p2])
    a2 = np.float32([[ww/3,0],[0,hh],[ww,hh]])
    M = cv2.getAffineTransform(a1, a2)  #仿射矩陣
    output = cv2.warpAffine(output1, M, (ww, hh))
    inv_M = cv2.invertAffineTransform(M)    #反仿射矩陣

    # m = cv2.getPerspectiveTransform(a1,a2)
    # output = cv2.warpPerspective(output, m, (ww, hh))
    # cv2.imshow('oxxostudio_7', output)
    # cv2.waitKey(1)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    output = cv2.dilate(output, kernel)  # 膨脹

    output = cv2.GaussianBlur(output, (5, 5), 0)  # 指定區域單位為 (5,5)
    # output = cv2.medianBlur(output, 5)  # 模糊化，去除雜訊
    # cv2.imshow('oxxostudio_4', output)
    # cv2.waitKey(0)

    output = cv2.erode(output, kernel)  # 侵蝕，將白色小圓點移除
    # cv2.imshow('oxxostudio_5', output)
    # cv2.waitKey(0)

    output = cv2.Canny(output, 150, 200)  # 偵測邊緣
    cv2.imshow('oxxostudio_6', output)
    cv2.waitKey(1)



    HOUGH_THRESHOLD, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP = 40, 15, 70
    lines = cv2.HoughLinesP(output, 1, np.pi / 180, HOUGH_THRESHOLD, None, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP)
    done, s1, s2, b1, b2 = 0, 0, 0, 0, 0
    img2 = img1.copy()
    co = (255, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            x1, y1, x2, y2 = l[0], l[1], l[2], l[3]
            # 計算直線的斜率與截距
            if x2 - x1 ==0:
                x2 = 1
                x1 = 0.99
            s = (y2 - y1) / (x2 - x1)  # s = slope
            b = y1 - s * x1  # y = s * x + b

            # cv2.circle(img2, (x1, y1), 3, (0, 255, 0), -1)  # 畫圓點 (-1 = 填滿)
            # cv2.circle(img2, (x2, y2), 3, (0, 0, 255), -1)  # 畫圓點 (-1 = 填滿)
            # cv2.line(img2, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # print("@", s, x1, y1, x2, y2, "done=", done)
            # cv2.imshow('oxxostudio_8', img2)
            # cv2.waitKey(0)

            if min(x1, x2) < 30 or max(x1, x2) > ww - 30:
                continue
            if s < 0 and s < s1:
                done = done | 1
                s1, b1 = s, b
            if s > 0 and s > s2:
                done = done | 2
                s2, b2 = s, b
            if done == 3:
                # y1, y2 = hh-r, hh-hh*0.175
                y1 = hh-r
                x = (int)(((y1-b1)/s1 + (y1-b2)/s2)/2)
                if abs(x-int(ww/2)-1) > 45: co = (0,0,255)
                cv2.line(img2, (x, y1), (x, y1-15), co, 2)

                p1 = [(int)((y1-b1)/s1), (int)(y1)]  
                p2 = [(int)((y2-b1)/s1), (int)(y2)]
                p3 = [(int)((y1-b2)/s2), (int)(y1)]  
                p4 = [(int)((y2-b2)/s2), (int)(y2)]
                zero = np.zeros((hh, ww, 3), dtype='uint8')  
                area = [p1, p2, p4, p3]  
                # print(p1)
                # print(p2)
                # print(p3)
                # print(p4)
                pts = np.array(area)
                mask = cv2.fillPoly(zero, [pts], (0, 50, 0))
                mask = cv2.warpAffine(mask, inv_M, (ww, hh))
                img2 = cv2.addWeighted(img2,1.0, mask,1.0, 0)
                #img2 = cv2.polylines(img2, [pts], True, (0,255,255), 2)  
                # cv2.imshow('oxxostudio_9', img2) ; cv2.waitKey(1)

    x, y = int(ww/2)-1, hh-r
    cv2.line(img2, (x, y), (x, y-12), (255,0,0), 2)

    # for i in range(1,10):
    #     x, y = int(ww/2)-1, hh-r
    #     cv2.line(img2, (x-i*15, y), (x-i*15, y-3), (0,255,0), 2)
    #     cv2.line(img2, (x+i*15, y), (x+i*15, y-3), (0,255,0), 2)
    cv2.imshow('oxxostudio', img2)
    out.write(img2)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()



