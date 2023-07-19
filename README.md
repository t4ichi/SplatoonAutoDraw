# スプラトゥーンのドット絵自動化
効率良く描くようにしました。

機材：Arduino Leonardo

## デモ
この絵だと全部描き終わるまで15分くらいかかった

![demo](https://github.com/t4ichi/SplatoonAutoDraw/assets/67674781/7031b89e-d76b-47f1-ad2c-afb92cfac11d)

## 手順


1.`generate-drawdata.py`を起動して320×120の画像ファイルを選択する

```
python3 generate-drawdata.py
```

2.生成された`data.h`で上書きする

3.Arduinoに書き込む

## 参考
https://yamamochi.com/splatoon3_autodotillust1/
