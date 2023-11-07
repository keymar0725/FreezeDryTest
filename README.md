# FreezeDryTest
FDテストcsvデータによるグラフ自動生成プログラム

KEYENCE 計測ソフトより生成したcsvファイルを読み込み、指定した時間ピッチ毎の温度を新しいリスト追加・プロットする。

また、以下の機能も実装している。
* センサー未接続状態（"BURNOUT"）をフィルタリング
* プロットピッチを指定し、グラフの解像度を変化させることが可能
* グラフ縦軸表示領域は、1軸：-40℃～100℃、2軸：50～120Pa
* センサー温度100℃以上および真空度200Pa以上はフィルタリング
* 出力名は「(csvファイル名)_(プロットピッチ)_(出力日).jpg」

現在、プロットピッチは1秒、1分、30分、1時間に対応。

# Requirement

* python3.10.5
* Pandas
* Matplotlib

# Installation

```bash
pip install pandas
pip install matplotlib
```

# Usage

git clone in any dirctory

```bash
git clone https://github.com/keymar0725/FreezeDryTest.git
```


make image of graph.

```bash
cd FreezeDryTest
python3 out_graph.py argv1 argv2
```

or

```bash
python3 ./(cloned dir)/FreezeDryTest/out_graph.py argv1 argv2
```
スクリプト実行に必要な引数は以下の二つである。
* argv1: Path to csv file (csvファイルへのパス。相対・絶対問わず)
* argv2: Plot pitch (グラフに記録する点のピッチ、csvファイルのデフォルトは1秒/ピッチである)
    ex)1sec = 1, 1min = 60, 30min = 1800, 1hour = 3600

# Example

```bash
python out_graph.py ./import/sasami.csv 60
```

or

```bash
python3 ./(cloned dir)/FreezeDryTest/out_graph.py ./import/sasami.csv 60
```

![0000_1min_20231106](https://github.com/keymar0725/FreezeDryTest/assets/47661559/40cfcc84-b949-44ac-a989-6001982e6386)

# Author

* Takahashi KEISUKE
* takahashikeisuke2525@gmail.com