# README
## 概略

| コンテナ | ベースイメージ | 用途 |
| :-- | :-- | :-- |
| lambda | public.ecr.aws/lambda/python:3.12 | Lambdaコンテナ。[コンテナイメージを使用した Lambda 関数の作成](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/images-create.html)| 
| localstack | localstack/localstack | LocalStackコンテナ。SSMパラメータストアを疑似的に再現。[LocalStack](https://www.localstack.cloud/)|

## 要追加ファイル

以下のファイルを挿入すること。

| パス | 記載概要 |
| :-- | :-- |
| ./.env | 環境変数 |
| ./localstack/.params.txt | SSMパラメータ(ローカル用)。主にシークレット情報を記載。|


**環境変数**

| 変数名 | 設定値 | 概説 |
| :-- | :-- | :-- |
| ENDPOINT_URL | http://localstack:4566 | localstackのエンドポイント。ローカルでのみ必要 |
| AWS_ACCESS_KEY_ID | dummy | 〃 |
| AWS_SECRET_ACCESS_KEY | dummy | 〃 |
| AWS_DEFAULT_REGION | dummy | 〃 |
| NOTION_DATABASE_QUERY_API_URL | https://api.notion.com/v1/databases/<Notion Database ID>/query | Notion APIパス |
| LINE_GROUP_ID　| <LINEのグループID> | 送信するグループID。取得方法：[参考](https://qiita.com/enbanbunbun123/items/2504687e4b6c13a289db) |


**SSMパラメータストア用変数**

| 変数名 | 概説 |
| :-- | :-- | 
| lambda/notion-notification/LINE_ACCESS_TOKEN | Line Messaging API アクセストークン |
| lambda/notion-notification/NOTION_API_TOKEN | Notion API インテグレーションシークレット |


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

注1：LocalStackにパラメータを読み込ませる処理が走るため、ログに``Ready.``が出るまではLambdaの実行を待つこと。

注2: LocalStack起動時に初期実行シェルが``No such file..``となる場合はシェルの改行コードをCRLFからLFにすること。

```
sed -i 's/\r//' localstack/init.sh
```

[参考その1](https://github.com/localstack/localstack/issues/7289#issuecomment-1367181135)

[参考その2](https://zenn.dev/db_tech/articles/1236c5e3a67c51)


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
