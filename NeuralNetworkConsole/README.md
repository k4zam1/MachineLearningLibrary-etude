# NNC_WebCameraJudge
NNCで作成した学習データをWebカメラでリアルタイム処理するスクリプト

main.py
実行にはTkinter,OpenCV,NNablaとWebカメラが接続されている必要があります。
実際に生成した新たな学習済みデータを利用する場合はprint(y.d)をするなどして、
どのように値を扱えばいいのか各自で考える必要があります。

また、生成されたネットワークによっては入力の形式が変更されている
可能性もあるため注意してください。
