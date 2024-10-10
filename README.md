# README
## 概略

| コンテナ | ベースイメージ | 用途 |
| :-- | :-- | :-- |
| lambda | public.ecr.aws/lambda/python:3.12 | Lambdaコンテナ。[コンテナイメージを使用した Lambda 関数の作成](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/images-create.html)| 
| localstack | localstack/localstack | LocalStackコンテナ。SSMパラメータストアを疑似的に再現。[LocalStack](https://www.localstack.cloud/)|

## ローカル起動方法
**前提環境**
- Docker
- Docker Compose

**初回起動**
ターミナルから以下を入力してコンテナ起動
```
docker-compose build
docker-compose up -d
```

注：LocalStackにパラメータを読み込ませる処理が走るため、ログに``Ready.``が出るまではLambdaの実行を待つこと。


**ソースコード更新時**
Lambdaのイメージは再起動しないとコードが反映されないため、lambdaコンテナのみ再起動が必要。

```
docker-compose up -d --no-deps --force-recreate lambda
```

**Lambdaの実行**
以下のコマンドでLambda起動.``{}``でPayload(JSON)を渡すことができる。

```
curl -d '{}' http://localhost:8080/2015-03-31/functions/function/invocations
```

## デプロイフロー
- Github mainブランチマージ
- webhookでcodebuild起動
- DockerビルドしてECRにPUSH
- CodebuildでLambdaにデプロイ
