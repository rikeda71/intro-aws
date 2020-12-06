# Hands-on 2: AWSでディープラーニングの計算を走らせる


## AMI(Amazon Machine Image)

- AMI(Amazon Machine Image) はマシンの初期状態のイメージ
- 何もインストールされていない標準状態のCentOSやUbuntuなどのOSから各種プログラムがインストール済みのものまである

- 以下のコマンドでAMIのリストを取得できる

```sh
$ aws ec2 describe-images --owners amazon
```

### DLAMI(Deep Learning Amazon Machine Image)

- ディープラーニングで頻繁に使われるプログラムが予めインストールされているAMIのこと
- `Tensorflow`, `PyTorch`などが予めインストールされている
- AMI: `ami-09c0c16fc46a29ed9`

- 以下のコマンドで詳細を閲覧できる

```sh
$ aws ec2 describe-images --owner amazon --image-ids 'ami-09c0c16fc46a29ed9'
```

## 実行方法

- ch04と同じなので割愛
