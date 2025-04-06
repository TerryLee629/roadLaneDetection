# roadLaneDetection
自駕車，以雷達、光達、感測器、GPS及電腦視覺等技術探測其周遭環境，並使其能夠自動駕駛至目的地。

這個專案將使用圖像處理技術，實作自駕車的車道偵測功能，使其能夠將車道位置用綠色色塊覆蓋標示，
在過程中了解需要使用那些圖像處理，與如何使用霍夫直線偵測來檢測直線。
簡單分成四步驟:

## 找出 ROI: Region Of Interest (關注區域)
設定座標去除圖片與車道不相關的景物
![](/img/Region.png)
取得ROI後將其使用仿設轉換，讓圖片呈現長方形，使圖片靠近消失點部分的車道更加清晰
