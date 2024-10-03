# OptHub Problems & Indicators

本リポジトリでは、複数のOptHubの問題や指標をまとめて管理しています。

## 問題

本リポジトリで管理している問題を以下に示します。各問題の詳細はIDのリンク先をご覧ください。

| ID     | Source Code | Docker Image |
| ------ | ----------- | ------------ |
| [sphere](https://opthub.ai/problems/sphere) | [opthub_problems/sphere](./opthub_problems/sphere/) | [opthub/problem-sphere](https://hub.docker.com/r/opthub/problem-sphere) |
| [elliptic](https://opthub.ai/problems/elliptic) | [opthub_problems/elliptic](./opthub_problems/elliptic/) | [opthub/problem-elliptic](https://hub.docker.com/r/opthub/problem-elliptic) |
| [rastrigin](https://opthub.ai/problems/rastrigin) | [opthub_problems/rastrigin](./opthub_problems/rastrigin/) | [opthub/problem-rastrigin](https://hub.docker.com/r/opthub/problem-rastrigin) |
| [rosenbrock](https://opthub.ai/problems/rosenbrock) | [opthub_problems/rosenbrock](./opthub_problems/rosenbrock/) | [opthub/problem-rosenbrock](https://hub.docker.com/r/opthub/problem-rosenbrock) |

## 指標

本リポジトリで管理している指標を以下に示します。各指標の詳細はIDのリンク先をご覧ください。

| ID     | Source Code | Docker Image |
| ------ | ----------- | ------------ |
| [best](https://opthub.ai/indicators/best) | [opthub_indicators/best](./opthub_indicators/best/) | [opthub/indicator-best](https://hub.docker.com/r/opthub/indicator-best) |
| [hypervolume](https://opthub.ai/indicators/hypervolume) | [opthub_indicators/hypervolume](./opthub_indicators/hypervolume/) | [opthub/indicator-hypervolume](https://hub.docker.com/r/opthub/indicator-hypervolume) |

## 開発者の方へ

### 環境設定

以下のステップに従って、環境設定をしてください。

1. 本リポジトリをclone
2. Poetryの設定
3. `poetry install`を実行
4. 推奨されたVS Codeの拡張機能をダウンロード
5. 他のパッケージとの競合を避けるため、以下のVS Codeの拡張機能を無効にする
    - ms-python.pylint
    - ms-python.black-formatter
    - ms-python.flake8
    - ms-python.isort

### 問題の作成
WIP

### 指標の作成
WIP

### コマンド一覧

利用可能なコマンドの一覧を以下に示す。`[type]`には`problem`もしくは`indicator`を代入し、`[name]`には問題もしくは指標のIDを入力してください。

#### テストの実行
```
$ make test-[type] NAME=[name]
```

#### イメージのビルド
```
$ make build-[type] NAME=[name]
```

#### イメージの公開
```
$ make push-[type] NAME=[name]
```
※ このコマンドは利用する前に、`docker login`を実行する必要があります。[認証情報](https://www.notion.so/opthub/Docker-Hub-91dc632599dd45e3bd1fcbad8ee71813?pvs=4)は管理者に権限をもらった上でアクセスできます。

## 連絡先 <a id="Contact"></a>

ご質問やご不明な点がございましたら、お気軽にお問い合わせください (Email: dev@opthub.ai)。

<img src="https://opthub.ai/assets/images/logo.svg" width="200">
