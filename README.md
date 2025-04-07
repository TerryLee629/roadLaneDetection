# RoadLaneDetection
自駕車，以雷達、光達、感測器、GPS及電腦視覺等技術探測其周遭環境，並使其能夠自動駕駛至目的地。

這個專案將使用圖像處理技術，實作自駕車的車道偵測功能，使其能夠將車道位置用綠色色塊覆蓋標示，
在過程中了解需要使用那些圖像處理，與如何使用霍夫直線偵測來檢測直線，最終達到檢測車道的目的。
簡單分成四步驟:

## 找出 ROI: Region Of Interest (關注區域)
- 設定座標去除圖片與車道不相關的景物。
<img src="/img/Region.png" width=500/>

## Affine transformation (仿設轉換)
- 取得ROI後將其使用仿設轉換，讓圖片呈現長方形，使圖片靠近消失點部分的車道更加清晰。

```
 a1 = np.float32([p4, p1, p2])
 a2 = np.float32([[ww/3,0],[0,hh],[ww,hh]])
 inv_M = cv2.invertAffineTransform(M)    #反仿射矩陣
```
<img src="/img/Affine.png" width=500/>
- 取得反仿設矩陣，用於之後將標示好的車道圖反仿設回原圖。

```
 inv_M = cv2.invertAffineTransform(M)    #反仿射矩陣
```
## 模糊化侵蝕 與 邊緣檢測
- 使用高斯模糊與侵蝕，使途中其他細節模糊消失，凸顯車道線。

```
 output = cv2.GaussianBlur(output, (5, 5), 0)  # 指定區域單位為 (5,5)
 output = cv2.erode(output, kernel)  # 侵蝕，將白色小圓點移除
```
<img src="/img/GaussianBlur.png" width=500/>
- 進行Canny邊緣檢測。

```
 output = cv2.Canny(output, 150, 200)  # 偵測邊緣
```
<img src="/img/CannyEdgepng.png" width=500/>
## 霍夫直線檢測
- 霍夫直線檢測得到途中直線點，並計算點中的斜率和截距，最後得到車道範圍的四個點，並用綠色色塊填滿。

```
 if done == 3:   #確定有兩條車道線圍出車道
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
    pts = np.array(area)
    mask = cv2.fillPoly(zero, [pts], (0, 50, 0))
    mask = cv2.warpAffine(mask, inv_M, (ww, hh))    #將反仿設矩陣放回到mask上使其貼合原圖
    img2 = cv2.addWeighted(img2,1.0, mask,1.0, 0)   #將車道範圍以綠色填滿
```
## 成果圖
<img src="/img/LineDetection.png" width=500/>
<img src="/img/LineDetection2.png" width=500/>
